import codecs
import json
import re


class Doc:
    def __init__(self, typ, textFile, searchType, prepend, header_id, header_description):
        self.type = typ
        self.textFile = textFile
        self.searchType = searchType
        self.json = dict()
        self.prepend = prepend
        self.header_id = header_id
        self.header_description = header_description


    def getJSON(self):
        with codecs.open(self.textFile.value, 'r', encoding="utf-8") as j_file:
            self.json = json.load(j_file, strict=False)

    def getListOfStringsFromJSON(self, urlObject):
        global p
        list_final = []

        l1 = self.__getList(urlObject.search_string_1, urlObject.regex)

        if (urlObject.search_string_2 == ""):
            list_final = l1

        else:
            l2 = self.__getList(urlObject.search_string_2, urlObject.regex)

            if urlObject.bool == "OR":
                list_final.extend(l1)
                list_final.extend(l2)
            elif urlObject.bool == "AND":
                list_final = list(set(l1) & set(l2))
            elif urlObject.bool == "NOT":
                list_final = list(set(l1) ^ set(l2))

        return list_final

    def __getList(self, search_string, regex):

        global p
        list_filename = []
        list_description = []
        list_other = []
        list_final = []

        if regex == "ON":
            p = re.compile(search_string)

        for file, content in self.json.items():
            if regex == "ON":  # regex
                x = p.search(content[self.header_id])
                if x is not None:
                    list_filename.append(
                        '"' + self.prepend + file + '"' + '\t' + content[
                            self.header_description])  # put at top of final list
                    continue

                x = p.search(content[self.header_description])
                if x is not None:
                    list_description.append(
                        ('"' + self.prepend + file + '"' + '\t' + content[
                            self.header_description]))  # put below filenames in final list
                    continue

                for cont, stuff in content.items():
                    x = p.search(stuff)
                    if x is not None:
                        list_other.append('"' + self.prepend + file + '"' + '\t' + content[
                            self.header_description])  # put at bottom of final list
                        continue
            else:
                if search_string in content[self.header_id]:
                    list_filename.append(
                        ('"' + self.prepend + file + '"' + '\t' + content[
                            self.header_description]))  # put at top of final list
                    continue

                if search_string in content[self.header_description]:
                    list_description.append(
                        ('"' + self.prepend + file + '"' + '\t' + content[
                            self.header_description]))  # put below filenames in final list
                    continue

                for cont, stuff in content.items():
                    if search_string in stuff:
                        list_other.append('"' + self.prepend + file + '"' + '\t' + content[
                            self.header_description])  # put at bottom of final list
                        continue

        list_final.extend(list_filename)
        list_final.extend(list_description)
        list_final.extend(list_other)
        return list_final



