# -*- coding: utf-8 -*-

from enum import Enum


class RequestMethod(Enum):

    Get = "GET"
    Post = "POST"
    Put = "PUT"
    Delete = "DELETE"
    Options = "OPTIONS"
