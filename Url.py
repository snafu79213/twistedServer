from enum import Enum
import html
from Types import boolType, searchType

class Url:
    def __init__(self, request):
        self.search_string_1 = self.__getString(b"search_string_1", request)
        self.bool_opt = boolType
        self.bool = self.__getString(b"bool", request)
        self.search_string_2 = self.__getString(b"search_string_2", request)
        self.type_opts = searchType
        self.type = self.__getString(b"type", request)
        self.regex = self.__getString(b"regex", request)
        self.page = self.__getString(b"page", request)
        if self.page == "":
            self.page = "1"
        self.link = '/?search_string_1=' + self.search_string_1.replace(" ", "+") + '&bool=' + self.bool + '&search_string_2=' + self.search_string_2.replace(" ", "+") + '&regex=' + self.regex + '&type=' + self.type.replace(" ", "+") + '&submit=Submit+Query&page='
        self.filename = self.__getString(b"filename", request)
        self.filename = self.filename.replace('"', '')
        self.client = request.client

    def __getString(self, b, request):
        t = ""
        try:
            t = html.escape(request.args[b][0].decode("utf-8"))
        except:
            pass
        return t.upper()
