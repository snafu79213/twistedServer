from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from Doc import Doc
from Url import Url
from Types import fileType, searchType, boolType, file
import socket
import subprocess
import datetime

import os

help_message = '<p>Usage: /?search_string_1=PATTERN&bool=OPERATOR&search_string_2=PATTERN&[REGEX="ON"]type=TYPE&submit=Submit+Query<br><br>' \
               'Search for PATTERN in each TYPE of file<br>' \
               'Example: /?search_string_1=0153979&bool=AND&search_string_2=test&type=NON-APPROVED+CLSI+DRAWINGS&submit=Submit+Query<br><br>' \
               'OPERATOR is one of the boolean operators AND OR or NOT<br><br>' \
               'TYPE is any of these types of files: NON-APPROVED+CLSI+DRAWINGS, APPROVED+CLSI+DRAWINGS, APPROVED+CLSII+DOCUMENTS, SERVICE+REQUESTS<br>' \
               'REGEX=ON makes sure the PATTERNS are used as regular expressions</p>'

MAX_VALUES = 1000
WEB_SERVER_PORT = 9999
FILE_SERVER_1_PORT = 8000
FILE_SERVER_1_PATH = "//CANOPUS/CAD/"
FILE_SERVER_2_PORT = 8001
FILE_SERVER_2_PATH = "//CANOPUS/MACHINE/COMMON/"
FILE_SERVER_3_PORT = 8002
FILE_SERVER_3_PATH = "//CANOPUS/RECORDS/DRAWINGS/"
FILE_SERVER_4_PORT = 8003
FILE_SERVER_4_PATH = "//CANOPUS/BMLCOM/"

class FormPage(Resource):
    def __init__(self):
        super().__init__()
        self.html = ""
        self.docs = []
        self.pages = 1

        self.docs.append(Doc(fileType.DWG, file.DWG, searchType.NonApprovedCLSIDrawings, "", "FILENAME", "TITLE OF THIS DRAWING"))
        self.docs.append(Doc(fileType.INVENTOR, file.IPT, searchType.NonApprovedCLSIDrawings, "", "FILENAME", "DESCRIPTION"))
        self.docs.append(Doc(fileType.INVENTOR, file.IDW, searchType.NonApprovedCLSIDrawings, "", "FILENAME", "DESCRIPTION"))
        self.docs.append(Doc(fileType.INVENTOR, file.IAM, searchType.NonApprovedCLSIDrawings, "", "FILENAME", "DESCRIPTION"))
        self.docs.append(Doc(fileType.PDFDocuments, file.PDFDocuments, searchType.ApprovedCLSIDocuments, "", "FILENAME", "DESCRIPTION"))
        self.docs.append(Doc(fileType.PDFDrawings, file.PDFDrawings, searchType.ApprovedCLSIDrawings, "", "FILENAME", "DESCRIPTION"))
        self.docs.append(Doc(fileType.ServiceRequests, file.ServiceRequests, searchType.ServiceRequests,
                              r"//srv-intranet-03/work/Lists/Work%20Orders/WODispForm.aspx?ID=", "ID", "LINKTITLE"))

        for doc in self.docs:
            doc.getJSON()

    def render_GET(self, request):
        return self.__render(request)

    def render_POST(self, request):
        return self.__render(request)

    def __render(self, request):
        self.url = Url(request)

        log = self.url.client.host + "\t" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\t" + self.url.search_string_1 + "\t" + self.url.bool + "\t" + self.url.search_string_2 + "\t" + self.url.type
        print(log)
        return self.__getWebPage()

    def __getWebPage(self):
        boolstr = ""
        typestr = ""
        regex = ""

        if self.url.filename is not "":
            i = 0

        self.__getHTML()

        for b in [e.value for e in boolType]:
            if b.upper() == self.url.bool:
                boolstr = boolstr + '<option value = "' + b.upper() + '" selected="selected">' + b.upper() + '</option>'
            else:
                boolstr = boolstr + '<option value = "' + b.upper() + '">' + b.upper() + '</option>'

        for b in [e.value for e in searchType]:
            if b.upper() == self.url.type:
                typestr = typestr + '<option value = "' + b.upper() + '" selected="selected">' + b.upper() + '</option>'
            else:
                typestr = typestr + '<option value = "' + b.upper() + '">' + b.upper() + '</option>'

        if self.url.regex == "ON":
            regex = "checked='checked'"

        if self.url.search_string_1 == "" and self.url.search_string_2 == "":
            self.html = help_message

        page = ""

        if int(self.url.page) > 1:
            page = "<a href=" + self.url.link + str(int(self.url.page) - 1) + ">prev</a>"

        if self.pages > int(self.url.page):
            page = page + "<a href=" + self.url.link + str(int(self.url.page) + 1) + "> next</a></div>"

        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title>CLSI Text Search Tool</title></head><body>"
                b"<form method='GET'>"
                b"<input type='text' name='search_string_1' value='" + self.url.search_string_1.encode("utf-8") +
                b"'>"
                b"<select name='bool'>"
                b"" + boolstr.encode("utf-8") +
                b"</select>"
                b"<input type='text' name='search_string_2' value='" + self.url.search_string_2.encode("utf-8") +
                b"'>"
                b"<input type='checkbox' name='regex' " + regex.encode("utf-8") +
                b">"
                b"<label for ='regex' >regex</label>"
                b"<select name='type'>"
                b"" + typestr.encode("utf-8") +
                b"</select>"
                b"<input type='submit' name='submit'>"
                b"</form>"
                b"" + self.html.encode("utf-8") +
                b"" + page.encode("utf-8") +
                b"</body>")



    def __getHTML(self):
        li = []
        self.html = ""

        if self.url.type not in [e.value for e in self.url.type_opts]:
            self.html = help_message

        for doc in self.docs:
            if self.url.type == doc.searchType.value:
                li.extend(doc.getListOfStringsFromJSON(self.url))

        li_count = len(li)
        self.pages = max(len(li)/MAX_VALUES, 1) # calculate the number of pages to include 'next' link if needed

        high = int(self.url.page) * MAX_VALUES  # used for upper end of list slice
        low = high - MAX_VALUES                 # used for lower end of list slice

        if low >= 0:                            # only slice if more than MAX_VALUES.
            li = li[low:high]
        else:
            li = []

        if len(li) == 0:
            self.html = "<p>" + str(li_count) + " Results</p>"
        else:
            self.html = "<p>" + str(low + 1) + "-" + str(low + len(li)) + " of " + str(li_count) + " Results</p>"

        n = socket.gethostname()
        h = socket.gethostbyname(n)
        for t in li:
            t = t.strip()
            x = t.split('\t')
            if self.url.type == self.url.type_opts.NonApprovedCLSIDrawings.value:
                x[0] = x[0].replace('"', '')
                x[0] = x[0].replace('\\', "/")
                x[0] = x[0].replace(FILE_SERVER_1_PATH,  str(h) + ':' + str(FILE_SERVER_1_PORT) + '/')
                x[0] = x[0].replace(FILE_SERVER_2_PATH, str(h) + ':' + str(FILE_SERVER_2_PORT) + '/')
                x[0] = x[0].replace(FILE_SERVER_4_PATH, str(h) + ':' + str(FILE_SERVER_4_PORT) + '/')
                self.html = self.html + '<a href = "http://' + x[0] + '" target="_blank"><pre>' + t + '</pre> </a>'

            elif self.url.type == self.url.type_opts.ApprovedCLSIDrawings.value:
                x = t.split('\t')
                x[0] = x[0].replace('"', '')
                x[0] = x[0].replace('\\', "/")
                x[0] = x[0].replace(FILE_SERVER_3_PATH, str(h) + ':' + str(FILE_SERVER_3_PORT) + '/')
                self.html = self.html + '<a href = "http://' + x[0] + '" target="_blank"><pre>' + t + '</pre> </a>'

            else:
                self.html = self.html + '<a href = ' + x[0] + ' target="_blank"><pre>' + t + '</pre> </a>'
        return self.html

subprocess.Popen("python -m http.server " + str(FILE_SERVER_1_PORT) + " -d " + FILE_SERVER_1_PATH)
subprocess.Popen("python -m http.server " + str(FILE_SERVER_2_PORT) + " -d " + FILE_SERVER_2_PATH)
subprocess.Popen("python -m http.server " + str(FILE_SERVER_3_PORT) + " -d " + FILE_SERVER_3_PATH)
subprocess.Popen("python -m http.server " + str(FILE_SERVER_4_PORT) + " -d " + FILE_SERVER_4_PATH)

root = Resource()
root.putChild(b"", FormPage())
factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, WEB_SERVER_PORT)
endpoint.listen(factory)
print("running")

reactor.run()