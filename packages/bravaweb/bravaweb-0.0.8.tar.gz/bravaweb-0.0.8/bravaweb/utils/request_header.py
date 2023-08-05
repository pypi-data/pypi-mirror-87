# -*- coding: utf-8 -*-

import configuration


def GetHeader(scope):
    headers = {}
    for item in scope["headers"]:
        headers[item[0].decode(configuration.api.encoding)] = item[1].decode(
            configuration.api.encoding)
    return headers
