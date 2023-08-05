# -*- coding: utf-8 -*-

from enum import Enum


class ResponseCode(Enum):

    OK = 200
    NoContent = 204
    NotFound = 404
    Invalid = 400
    Forbidden = 403
    PreconditionFailed = 412
    InternalError = 500
    Redirect = 302
    Permanent = 301
    Temporary = 307
    MethodNotAllowed = 405
    Unauthorized = 401

    def __str__(self):
        return "%s %s" % (self.value, self.description)

    @property
    def description(self):
        codes = {
            # Informational.
            100: "Continue",
            101: "Switching Protocols",
            102: "Processing",
            103: "Checkpoint",
            122: "Uri Too Long",
            200: "Ok",
            201: "Created",
            202: "Accepted",
            203: "Non Authoritative Info",
            204: "No Content",
            205: "Reset Content",
            206: "Partial Content",
            207: "Multi Status",
            208: "Already Reported",
            226: "Im Used",

            # Redirection.
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            304: "Not Modified",
            305: "Use Proxy",
            306: "Switch Proxy",
            307: "Temporary Redirect",
            308: "Permanent Redirect",

            # Client Error.
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Request Entity Too Large",
            414: "Request Uri Too Large",
            415: "Unsupported Media Type",
            416: "Requested Range Not Satisfiable",
            417: "Expectation Failed",
            418: "Im A Teapot",
            421: "Misdirected Request",
            422: "Unprocessable Entity",
            423: "Locked",
            424: "Failed Dependency",
            425: "Unordered Collection",
            426: "Upgrade Required",
            428: "Precondition Required",
            429: "Too Many Requests",
            431: "Header Fields Too Large",
            444: "No Response",
            449: "Retry With",
            450: "Blocked By Windows Parental Controls",
            451: "Unavailable For Legal Reasons",
            499: "Client Closed Request",

            # Server Error.
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            505: "Http Version Not Supported",
            506: "Variant Also Negotiates",
            507: "Insufficient Storage",
            509: "Bandwidth Limit Exceeded",
            510: "Not Extended",
            511: "Network Authentication Required",
        }
        return codes[self.value]

    @property
    def code(self):
        return self.value
