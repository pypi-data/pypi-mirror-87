#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import logging
import socket
from queue import Queue
from threading import Thread, Event
from typing import TYPE_CHECKING
from skywalking import config, plugins
from skywalking.agent.protocol import Protocol
from skywalking.config import *
if TYPE_CHECKING:
    from skywalking.trace.context import Segment

logger = logging.getLogger(__name__)
disable_plugins = {'sw_django',
                   'sw_elasticsearch',
                   'sw_flask',
                   'sw_http_server',
                   'sw_kafka',
                   'sw_pymongo',
                   'sw_rabbitmq',
                   'sw_tornado',
                   'sw_urllib_request'}
service_name = os.environ.get('service_name', 'not configured')
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


def __heartbeat():
    while not __finished.is_set():
        if connected():
            __protocol.heartbeat()

        __finished.wait(30 if connected() else 3)


def __report():
    while not __finished.is_set():
        if connected():
            __protocol.report(__queue)  # is blocking actually

        __finished.wait(1)


__heartbeat_thread = Thread(name='HeartbeatThread', target=__heartbeat, daemon=True)
__report_thread = Thread(name='ReportThread', target=__report, daemon=True)
__queue = Queue(maxsize=10000)
__finished = Event()
__protocol = Protocol()  # type: Protocol
__started = False


def __init():
    global __protocol
    if config.protocol == 'grpc':
        from skywalking.agent.protocol.grpc import GrpcProtocol
        __protocol = GrpcProtocol()
    elif config.protocol == 'http':
        from skywalking.agent.protocol.http import HttpProtocol
        __protocol = HttpProtocol()
    elif config.protocol == "kafka":
        from skywalking.agent.protocol.kafka import KafkaProtocol
        __protocol = KafkaProtocol()

    plugins.install()


def start():
    global __started
    if __started:
        raise RuntimeError('the agent can only be started once')
    from skywalking import loggings
    loggings.init()
    __started = True
    config.init()
    config.deserialize(dict(disable_plugins=disable_plugins,
                            service_instance=f'{config.service_name}@{hostname}'))
    __init()
    __heartbeat_thread.start()
    __report_thread.start()


def stop():
    __finished.set()


def started():
    return __started


def connected():
    return __protocol.connected()


def archive(segment: 'Segment'):
    if __queue.full():
        logger.warning('the queue is full, the segment will be abandoned')
        return

    __queue.put(segment)
