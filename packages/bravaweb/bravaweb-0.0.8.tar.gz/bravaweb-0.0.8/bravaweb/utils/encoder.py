# -*- coding: utf-8 -*-

import json
import datetime
import decimal

import configuration

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            if isinstance(o, decimal.Decimal):
                return float(o)
            if isinstance(o, datetime.datetime):
                return o.strftime(configuration.api.date_format)
            if isinstance(o, bytes):
                return o.decode('utf-8')
            return super(CustomEncoder, self).default(o)
        except Exception as e:
            raise e
