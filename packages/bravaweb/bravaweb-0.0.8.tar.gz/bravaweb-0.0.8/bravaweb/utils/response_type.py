# -*- coding: utf-8 -*-

import configuration

from enum import Enum


class ResponseType(Enum):

    # Application
    Edi = 1
    Edifact = 2
    JavaScript = 3
    OctetStream = 4
    Ogg = 5
    Pdf = 6
    Xhtml = 7
    Flash = 8
    Json = 9
    Ld_Json = 10
    Xml = 11
    Zip = 12

    # AUDIO
    MpegAudio = 13
    Wma = 14
    RealAudio = 15
    Wav = 16

    # IMAGE
    Gif = 17
    Jpg = 18
    Png = 19
    Tiff = 20
    MsIcon = 21
    Icon = 22
    Djvu = 23
    Svg = 24

    # MULTIPART
    MultipartMixex = 25
    MultipartAlternative = 26
    MultipartRelated = 27

    # PLAIN TEXT
    Css = 28
    Csv = 29
    Html = 30
    TextJavaScript = 31
    TextPlain = 32
    TextXml = 33

    # video
    MpegVideo = 34
    Mp4 = 35
    Quicktime = 36
    Wmv = 37
    MsVideo = 38
    Flv = 39
    Webm = 40

    # VND
    OpenDocument = 41
    OpenSpreadSheet = 42
    OpenPresentation = 43
    OpenGraphics = 44
    MsExcel = 45
    MsExcelSheet = 46
    MsPowerpoint = 47
    MsPowerpointPresentation = 48
    MsWord = 49
    MsWord_document = 50
    MozillaXul = 51

    def __str__(self):
        return "Content-Type: %s" % self.description

    @property
    def description(self):
        codes = {
            # APPLICATION
            1: "application/EDI-X12",
            2: "application/EDIFACT",
            3: "application/javascript; charset={charset}",
            4: "application/octet-stream",
            5: "application/ogg",
            6: "application/pdf",
            7: "application/xhtml+xml; charset={charset}",
            8: "application/x-shockwave-flash",
            9: "application/json; charset={charset}",
            10: "application/ld+json; charset={charset}",
            11: "application/xml; charset={charset}",
            12: "application/zip",
            # AUDIO
            13: "audio/mpeg",
            14: "audio/x-ms-wma",
            15: "audio/vnd.rn-realaudio",
            16: "audio/x-wav",
            # IMAGE
            17: "image/gif",
            18: "image/jpeg",
            19: "image/png",
            20: "image/tiff",
            21: "image/vnd.microsoft.icon",
            22: "image/x-icon",
            23: "image/vnd.djvu",
            24: "image/svg+xml",
            # MULTIPART
            25: "multipart/mixed",
            26: "multipart/alternative",
            27: "multipart/related",
            # PLAIN TEXT
            28: "text/css; charset={charset}",
            29: "text/csv; charset={charset}",
            30: "text/html; charset={charset}",
            31: "text/javascript; charset={charset}",
            32: "text/plain; charset={charset}",
            33: "text/xml; charset={charset}",
            # VIDEO
            34: "video/mpeg",
            35: "video/mp4",
            36: "video/quicktime",
            37: "video/x-ms-wmv",
            38: "video/x-msvideo",
            39: "video/x-flv",
            40: "video/webm",
            # VND
            41: "application/vnd.oasis.opendocument.text",
            42: "application/vnd.oasis.opendocument.spreadsheet",
            43: "application/vnd.oasis.opendocument.presentation",
            44: "application/vnd.oasis.opendocument.graphics",
            45: "application/vnd.ms-excel",
            46: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            47: "application/vnd.ms-powerpoint",
            48: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            49: "application/msword",
            50: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            51: "application/vnd.mozilla.xul+xml",
        }
        return codes[self.value].format(charset=configuration.api.encoding)

    @property
    def extension(self):
        exts = {
            # APPLICATION
            1: "",
            2: "",
            3: "js",
            4: "bin",
            5: "ogg",
            6: "pdf",
            7: "xhtml",
            8: "swf",
            9: "json",
            10: "json",
            11: "xml",
            12: "zip",
            # AUDIO
            13: "mpeg",
            14: "wma",
            15: "ra",
            16: "wav",
            # IMAGE
            17: "gif",
            18: "jpg",
            19: "png",
            20: "tiff",
            21: "ico",
            22: "ico",
            23: "djvu",
            24: "svg",
            # MULTIPART
            25: "",
            26: "",
            27: "",
            # PLAIN TEXT
            28: "css",
            29: "csv",
            30: "html",
            31: "js",
            32: "txt",
            33: "xml",
            # VIDEO
            34: "mpeg",
            35: "mp4",
            36: "mov",
            37: "wmv",
            38: "avi",
            39: "flv",
            40: "webm",
            # VND
            41: "odt",
            42: "ods",
            43: "pdp",
            44: "odg",
            45: "xlsx",
            46: "ods",
            47: "ppt",
            48: "ppt",
            49: "docx",
            50: "docx",
            51: "xml",
        }
        return exts[self.value]
