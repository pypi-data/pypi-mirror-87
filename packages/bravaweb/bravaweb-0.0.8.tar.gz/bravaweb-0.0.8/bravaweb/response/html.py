
from mako.template import Template
from mako.lookup import TemplateLookup

# configuration
import configuration
import os

from bravaweb.response.lib.object import ResponseObject


class Html(ResponseObject):

    def FileName(self, **args):
        route = args["route"]
        action = args["action"]
        route[0] = "views"
        file = "{}/{}.html".format("/".join(route), action)
        if not os.path.exists("{}/{}".format(configuration.api.directory, file)):
            file = "views/shared/default.html"
        return file

    def Response(self, data, **args):

        _data = data

        _mylookup = TemplateLookup(directories=[''])

        _filename = self.FileName(**args)
        #args["template"] if "template" in args else "views/errors/default.html"

        template = Template(filename=_filename, lookup=_mylookup, input_encoding=configuration.api.encoding,
                            output_encoding=configuration.api.encoding, default_filters=['decode.{}'.format(configuration.api.encoding)], encoding_errors='replace')
        return template.render(data=_data)
