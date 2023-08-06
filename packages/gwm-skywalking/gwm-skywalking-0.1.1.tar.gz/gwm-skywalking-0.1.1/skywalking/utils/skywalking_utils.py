import os
from enum import Enum
from inspect import isawaitable
from skywalking import Layer, agent
from skywalking.trace import tags
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import get_context
from skywalking.trace.tags import Tag
from skywalking import Component
from fastapi import Request



async def skywalking_record(request: Request, call_next):
    context = get_context()
    carrier = Carrier()
    for item in carrier:
        if item.key.capitalize() in request.headers:
            item.val = request.headers[item.key.capitalize()]
    with context.new_entry_span(op=f'{request.url}', carrier=carrier) as span:
        span.layer = Layer.Http
        span.component = Component.FastApi
        peer = [request.client.host, request.client.port]
        span.peer = '{0}:{1}'.format(*peer)
        span.tag(Tag(key=tags.HttpMethod, val=request.method, overridable=False))
        span.tag(
            Tag(key=tags.HttpUrl, val=request.url.path, overridable=False))
        response = await call_next(request)
        span.tag(Tag(key=tags.HttpStatus, val=response.status_code, overridable=False))
        if isawaitable(response):
            response = await response
        if response.status_code >= 400:
            span.error_occurred = True
    return response


def skywalking_startup():
    agent.start()


def skywalking_shutdown():
    agent.stop()

