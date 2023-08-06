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
import logging
from skywalking import Layer, Component
from skywalking.trace import tags
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import get_context
from skywalking.trace.tags import Tag
from rocketmq.client import ffi_check, dll, _to_bytes, ReceivedMessage, ConsumeStatus


logger = logging.getLogger(__name__)


def install():
    from rocketmq.client import Producer, PushConsumer, TransactionMQProducer, Message

    _send_sync = Producer.send_sync
    _send_oneway = Producer.send_oneway
    _send_orderly_with_sharding_key = Producer.send_orderly_with_sharding_key
    _set_name_server_address = Producer.set_name_server_address

    Producer.send_sync = _sw__send_sync(_send_sync)
    Producer.send_oneway = _sw__send_oneway(_send_oneway)
    Producer.send_orderly_with_sharding_key = _sw__send_orderly_with_sharding_key(_send_orderly_with_sharding_key)
    Producer.set_name_server_address = _sw__set_name_server_address_producer
    
    
    _subscribe = PushConsumer.subscribe
    
    PushConsumer.set_name_server_address = _sw__set_name_server_address_consumer
    PushConsumer.subscribe = _sw_subscribe


def _sw__set_name_server_address_producer(self, addr):
    self.addr = addr
    ffi_check(dll.SetProducerNameServerAddress(self._handle, _to_bytes(addr)))


def _sw__set_name_server_address_consumer(self, addr):
    self.addr = addr
    ffi_check(dll.SetPushConsumerNameServerAddress(self._handle, _to_bytes(addr)))
        

def _sw__send_sync(_send_sync):
    def _send_sync_handle(self, msg):
        peer = self.addr
        context = get_context()
        carrier = Carrier()
        recv_msg = ReceivedMessage(msg)
        topic = recv_msg.topic
        with context.new_exit_span(op="RocketMQ/" + topic + "/Producer" or "/",
                                   peer=peer, carrier=carrier) as span:
            span.layer = Layer.MQ
            span.component = Component.RocketMQProducer
            for item in carrier:
                msg.set_property(item.key, item.val)
            try:
                res = _send_sync(self, msg)
                span.tag(Tag(key=tags.MqBroker, val=peer))
                span.tag(Tag(key=tags.MqTopic, val=topic))
            except BaseException as e:
                span.raised()
                raise e
            return res
    return _send_sync_handle


def _sw__send_oneway(_send_oneway):
    def _send_oneway_handle(self, msg):
        peer = self.addr
        context = get_context()
        carrier = Carrier()
        recv_msg = ReceivedMessage(msg)
        with context.new_exit_span(op="RocketMQ/" + recv_msg.topic + "/Producer" or "/",
                                   peer=peer, carrier=carrier) as span:
            span.layer = Layer.MQ
            span.component = Component.RocketMQProducer
            for item in carrier:
                msg.set_property(item.key, item.val)
            try:
                _send_oneway(self, msg)
                span.tag(Tag(key=tags.MqBroker, val=peer))
                span.tag(Tag(key=tags.MqTopic, val=topic))
            except BaseException as e:
                span.raised()
                raise e
    return _send_oneway_handle


def _sw__send_orderly_with_sharding_key(_send_orderly_with_sharding_key):
    def _send_orderly_with_sharding_key_handle(self, msg, sharding_key):
        peer = self.addr
        context = get_context()
        carrier = Carrier()
        recv_msg = ReceivedMessage(msg)
        with context.new_exit_span(op="RocketMQ/Topic/" + recv_msg.topic + "/Producer" or "/",
                                   peer=peer, carrier=carrier) as span:
            span.layer = Layer.MQ
            span.component = Component.RocketMQProducer
            for item in carrier:
                msg.set_property(item.key, item.val)
            try:
                res = _send_orderly_with_sharding_key(self, msg, sharding_key)
                span.tag(Tag(key=tags.MqBroker, val=peer))
                span.tag(Tag(key=tags.MqTopic, val=topic))
            except BaseException as e:
                span.raised()
                raise e
            return res
    return _send_orderly_with_sharding_key_handle
    


def _sw_subscribe(self, topic, callback, expression='*'):
    def _on_message(consumer, msg):
        peer = self.addr
        context = get_context()
        carrier = Carrier()
        msg = ReceivedMessage(msg)
        for item in carrier:
            if msg[item.key]:
                item.val = msg[item.key].decode('utf-8')
        with context.new_entry_span(op="RocketMQ" + topic + "/Consumer" or "", carrier=carrier, peer=peer) as span:
            span.layer = Layer.MQ
            span.component = Component.RocketMQConsumer
            exc = None
            try:
                consume_result = callback(msg)
                if consume_result != ConsumeStatus.CONSUME_SUCCESS and consume_result != ConsumeStatus.RECONSUME_LATER:
                    raise ValueError('Consume status error, please use enum \'ConsumeStatus\' as response')
                return consume_result
            except BaseException as e:
                exc = e
                return ConsumeStatus.RECONSUME_LATER
            finally:
                if exc:
                    span.raised()
                    raise exc
    ffi_check(dll.Subscribe(self._handle, _to_bytes(topic), _to_bytes(expression)))
    self._register_callback(_on_message)
