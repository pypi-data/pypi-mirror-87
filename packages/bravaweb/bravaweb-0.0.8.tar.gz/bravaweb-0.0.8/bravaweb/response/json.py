
import json
import datetime
import decimal

# configuration
import configuration

from bravaweb.response.lib.object import ResponseObject
from bravaweb.utils.encoder import CustomEncoder

class Json(ResponseObject):

    def Response(self, data, success=True, **args):
        _data = data

        _template = dict(self.template)
        _template["date"] = datetime.datetime.now()
        _template["itens"] = 0
        if success:
            if not _data:
                _data = False

            if hasattr(_data, 'toJSON'):
                _data = _data.toJSON()

            elif isinstance(_data, dict):
                _data = _data

            _template["data"] = _data
            _template["date"] = datetime.datetime.now()
            _template["itens"] = len(_data) if isinstance(_data, list) else 1

            if "token" in args:
                _template["token"] = args["token"]

            if "task" in args and args["task"]:
                _template["task"] = args["task"]
        else:
            _template["success"] = False
            _template["date"] = datetime.datetime.now()
            _template["error"] = args["error"] if "error" in args else "Invalid Request"

        return json.dumps(_template, cls=CustomEncoder, indent=4).encode(configuration.api.encoding)
