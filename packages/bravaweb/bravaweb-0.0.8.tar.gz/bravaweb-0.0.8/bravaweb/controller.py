# -*- coding: utf-8 -*-

from bravaweb.security.methods import *
from bravaweb.security.decorator import require
from bravaweb.utils import ResponseType, ResponseCode, RequestMethod
from bravaweb.response import *

from datetime import datetime
import decimal

import configuration

class Controller(object):

    def __init__(self, envirom):
        self.enviroment = envirom
        super(Controller, self).__init__()

    # TODO VERIFICAR SE ESTA USANDO ELE, O ENTER OU EXIT
    def __del__(self):
        pass

    async def NotAllowed(self):

        content = "405: Method not allowed".encode(configuration.api.encoding)

        _headers = [
            (b'content-type', b'text/html; charset=utf-8'),
            (b"Content-Length", str(len(content)).encode(configuration.api.encoding)),
            (b"Accept-Ranges", b"bytes"),
            (b"X-Frame-Options", b"Deny")
        ]

        if self.enviroment.origin:
            _headers.append((b"Access-Control-Allow-Origin", self.enviroment.origin.encode(configuration.api.encoding)))

        await self.enviroment.send({
            'type': 'http.response.start',
            'status': ResponseCode.MethodNotAllowed.code,
            'headers': _headers
        })

        await self.enviroment.send({
            'type': 'http.response.body',
            'body': content
        })

    async def Unauthorized(self):

        content = "401: Unauthorized".encode(configuration.api.encoding)

        _headers = [
            (b'content-type', b'text/html; charset=utf-8'),
            (b"Content-Length", str(len(content)).encode(configuration.api.encoding)),
            (b"Accept-Ranges", b"bytes"),
            (b"X-Frame-Options", b"Deny")
        ]

        if self.enviroment.origin:
            _headers.append((b"Access-Control-Allow-Origin", self.enviroment.origin.encode(configuration.api.encoding)))

        await self.enviroment.send({
            'type': 'http.response.start',
            'status': ResponseCode.Unauthorized.code,
            'headers': _headers
        })

        await self.enviroment.send({
            'type': 'http.response.body',
            'body': content
        })

    async def NotFound(self):

        content = "404: Not Found".encode(configuration.api.encoding)

        _headers = [
            (b'content-type', b'text/html; charset=utf-8'),
            (b"Content-Length", str(len(content)).encode(configuration.api.encoding)),
            (b"Accept-Ranges", b"bytes"),
            (b"X-Frame-Options", b"Deny")
        ]

        if self.enviroment.origin:
            _headers.append((b"Access-Control-Allow-Origin", self.enviroment.origin.encode(configuration.api.encoding)))

        await self.enviroment.send({
            'type': 'http.response.start',
            'status': ResponseCode.NotFound.code,
            'headers': _headers
        })

        await self.enviroment.send({
            'type': 'http.response.body',
            'body': content
        })

    async def NoContent(self):

        content = "204: No Content".encode(configuration.api.encoding)

        _headers = [
            (b'content-type', b'text/html; charset=utf-8'),
            (b"Content-Length", str(len(content)).encode(configuration.api.encoding)),
            (b"Accept-Ranges", b"bytes"),
            (b"X-Frame-Options", b"Deny")
        ]

        if self.enviroment.origin:
            _headers.append((b"Access-Control-Allow-Origin", self.enviroment.origin.encode(configuration.api.encoding)))

        await self.enviroment.send({
            'type': 'http.response.start',
            'status': ResponseCode.NoContent.code,
            'headers': _headers
        })

        await self.enviroment.send({
            'type': 'http.response.body',
            'body': content
        })

    async def PreconditionFailed(self, errors):

        content = "412: Precondition Failed".encode(configuration.api.encoding)

        _headers = [
            (b'content-type', b'text/html; charset=utf-8'),
            (b"Content-Length", str(len(content)).encode(configuration.api.encoding)),
            (b"Accept-Ranges", b"bytes"),
            (b"X-Frame-Options", b"Deny")
        ]

        if self.enviroment.origin:
            _headers.append((b"Access-Control-Allow-Origin", self.enviroment.origin.encode(configuration.api.encoding)))

        await self.enviroment.send({
            'type': 'http.response.start',
            'status': ResponseCode.PreconditionFailed.code,
            'headers': _headers
        })

        await self.enviroment.send({
            'type': 'http.response.body',
            'body': content
        })

    async def InternalError(self):

        content = "500: Internal Error".encode(configuration.api.encoding)

        _headers = [
            (b'content-type', b'text/html; charset=utf-8'),
            (b"Content-Length", str(len(content)).encode(configuration.api.encoding)),
            (b"Accept-Ranges", b"bytes"),
            (b"X-Frame-Options", b"Deny")
        ]

        if self.enviroment.origin:
            _headers.append((b"Access-Control-Allow-Origin", self.enviroment.origin.encode(configuration.api.encoding)))

        await self.enviroment.send({
            'type': 'http.response.start',
            'status': ResponseCode.InternalError.code,
            'headers': _headers
        })

        await self.enviroment.send({
            'type': 'http.response.body',
            'body': content
        })
