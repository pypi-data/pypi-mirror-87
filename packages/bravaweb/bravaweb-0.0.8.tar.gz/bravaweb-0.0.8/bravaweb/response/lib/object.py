

import datetime
import configuration

from bravaweb.utils import ResponseType


class ResponseObject():

    def __init__(self):
        self.extension = ResponseType[self.__class__.__name__].extension
        self.content_type = ResponseType[self.__class__.__name__].description
        self.header = ("Content-Type".encode(configuration.api.encoding),
                       self.content_type.encode(configuration.api.encoding))
        try:
            self.template = getattr(
                configuration.templates, self.__class__.__name__)
        except AttributeError:
            self.template = None

    def Response(self, data, **args):
        return data
