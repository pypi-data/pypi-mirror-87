# -*- coding: utf-8 -*-

# Third Part Imports

# Basics Imports
import configuration

# Utils
from bravaweb.utils import GetHeader

# Security
import bravaweb.security as Security

# Enviroment
from bravaweb.enviroment import Enviroment

# Error Tratament
import traceback

# App Boot Time
from datetime import datetime

boot_time = datetime.now()

async def App(scope, receive, send):

    headers = GetHeader(scope)

    if scope["method"] == "OPTIONS":
        await Security.origin.Options(headers, send)

    elif Security.origin.Static(scope):
        await Security.origin.NotFound(send)

    elif Security.origin.Permitted(headers, scope):

        try:

            envirom = Enviroment(headers, scope, receive, send)
            await envirom.ReceiveBody()
            await envirom.Response()

        except Exception as e:
            print("\n\nError: {}\n\n-- TRACEBACK --\n\n{}\n\n".format(e, traceback.format_exc()))
    else:
        await Security.origin.Forbidden(send)
