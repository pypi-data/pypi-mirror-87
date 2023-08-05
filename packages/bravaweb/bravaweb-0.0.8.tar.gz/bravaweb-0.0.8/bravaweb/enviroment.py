# -*- coding: utf-8 -*-

# Third Part
import re
import jwt
import json
import urllib.parse

# configuration
import configuration

# Utils
from bravaweb.utils import GetBody, RequestMethod

# Secutiry
from bravaweb.security.request_params import ValidRequestParams


class Enviroment():

    def __init__(self, headers, scope, receive, send):

        # Init Params
        self.headers = headers
        self.scope = scope
        self.send = send
        self.receive = receive

        # Default Params
        self.origin = headers["origin"] if "origin" in headers else None
        self.remote_ip = scope['client'][0]
        self.remote_uuid = headers['uuid'] if "uuid" in headers else None
        self.browser = headers["user-agent"] if "user-agent" in headers else None
        self.accept_encoding = headers["accept-encoding"] if "accept-encoding" in headers else None
        self.remote = {
            "ip": self.remote_ip,
            'uuid' : self.remote_uuid,
            "browser": self.browser,
            "accept": self.accept_encoding
            }
        self.method = RequestMethod(scope["method"])
        self.response_type = None

        # Authorization
        self.authorization = headers["authorization"] if "authorization" in headers else None
        self.auth_token = None

        try:
            self.bearer = jwt.decode(headers["authorization"].replace(
                'Bearer ', ''), configuration.api.token, algorithms='HS256') if self.authorization is not None else None
        except:
            self.bearer = {}

        # Content Length
        self.content_length = int(
            headers['content-length']) if "content-length" in headers else 0

        # Query String
        self.get = {}
        for item in scope["query_string"].decode(configuration.api.encoding).split("&"):
            if "=" in item:
                item_name = urllib.parse.unquote(item.split("=")[0])
                item_value = urllib.parse.unquote(item.split("=")[1])
                if item_name.find("[") >= 0  and item_name.find("]") >= 0:
                    object_name, field_name = item_name.split("[")[0], item_name.split("[")[1].replace("]","")
                    if object_name in self.get:
                        self.get[object_name][field_name] = item_value
                    else:
                        self.get[object_name] = {field_name : item_value}
                else:
                    self.get[item_name] = item_value
            else:
                item_name = urllib.parse.unquote(item)

        # Post
        self.post = {}

        # Validate Route
        self.controller, self.area, self.module, self.action, self.id = None, None, "default", "index", None

        # Route Rule
        RouteRule = [route for route in configuration.api.routes
                     if bool(re.match(route[1], scope["path"]))][0][0]

        # Request Route
        RequestRoute = scope["path"][1:].split("/")
        for index, attr in enumerate(RouteRule.split("/")):
            # If Attribute was defined
            if re.match("\{.*?\}", attr):
                try:
                    self.__setattr__(
                        attr[attr.find("{") + 1:attr.find("}")], RequestRoute[index])
                except IndexError:
                    pass
            # Else Pattern
            elif index == 0:
                self.controller = attr
            elif index == 1:
                self.area = attr
            elif index == 2:
                self.module = attr
            elif index == 3:
                self.action = attr
            elif index == 4:
                self.id = attr

        self.route = ["controllers"]

        if self.controller:
            self.route.append(self.controller)
        if self.area:
            self.route.append(self.area)
        if self.module:
            self.route.append(self.module)

        self.klass = "{}Controller".format(self.route[-1].capitalize())

    async def ReceiveBody(self):
        self.body = await GetBody(self.receive)

        # Post
        if len(self.body) > 0:
            try:
                self.post = json.loads(
                    self.body.decode(configuration.api.encoding))
            except ValueError:
                for item in self.body.decode(configuration.api.encoding).split("&"):
                    if "=" in item:
                        item_name = urllib.parse.unquote(item.split("=")[0])
                        item_value = urllib.parse.unquote(item.split("=")[1])
                        if item_name.find("[") >= 0  and item_name.find("]") >= 0:
                            object_name, field_name = item_name.split("[")[0], item_name.split("[")[1].replace("]","")
                            if object_name in self.post:
                                self.post[object_name][field_name] = item_value
                            else:
                                self.post[object_name] = {field_name : item_value}
                        else:
                            self.post[item_name] = item_value
                    else:
                        item_name = urllib.parse.unquote(item)

        # Union Get and Post Params
        self.request = {**self.get, **self.post}

    async def Response(self):

        # Load Module
        try:
            _module = __import__(".".join(self.route), fromlist=[self.klass])
        except Exception as e:
            raise e

        # Load Class
        try:
            _class = _module.__getattribute__(self.klass)(envirom=self)
        except Exception as e:
            raise e

        # Load Action
        try:
            _action = _class.__getattribute__(self.action)
        except AttributeError:
            # 404 Not Found
            _action = _class.__getattribute__("NotFound")
        except Exception as e:
            raise e

        # Validate Request Action
        try:
            params, errors = ValidRequestParams(self, _action, _class)
            if len(errors) > 0:
                _action = _class.__getattribute__("PreconditionFailed")
                params = {'errors': errors}
        except Exception as e:
            raise e

        # Execute Action
        try:
            await _action(**params)
        except Exception as e:
            raise e
