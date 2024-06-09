import json
import os

from errorlib import *

kardfm_supports = [
    "json"
]

class kardfm:
    def __init__(self, dfmname, path="local") -> None:
        if path == "local":
            path = dfmname+'\\'
        os.makedirs(path, exist_ok=True)
        self.path = path

        os.makedirs(path + "kardfm_camp\\", exist_ok=True)
        with open(self.path + "kardfm_camp\\docdata.json","w") as f:
            json.dump({}, f)
        self.docdatapath = self.path + "kardfm_camp\\docdata.json"

        self.dfmname = dfmname
        self.data = None
        
        self.dfname = None
        self.dftype = None

    def createdoc(self, docname, doctype="json"):
        if not (type(docname) == str):
            raise karDFM_TypeError(f"TypeError : {docname} passed in for docname.\nOnly string data type is accepted for docname arg.")
        else:
            pass
        
        if not (doctype in kardfm_supports):
            raise karDFM_TypeDefError(f"TypeDefError : {doctype} is not supported. \nOnly pass in document types which are supported by karDFM")
        else:
            pass

        if doctype == "json":
            docpath = self.path + docname + ".json"
            with open(docpath, "w") as f:
                json.dump(None, f)

        with open(self.path + "kardfm_camp\\docdata.json","r") as f:
            data = json.load(f)

        data[docname] = {"doctype":doctype}

        with open(self.path + "kardfm_camp\\docdata.json", 'w') as f:
            json.dump(data,f,indent=3)

        self.loaddoc(docname)

    def loaddoc(self, docname):
        if not (type(docname) == str):
            raise karDFM_TypeError(f"TypeError : {docname} passed in for docname.\nOnly string data type is accepted for docname arg.")
        else:
            pass

        with open(self.docdatapath,'r') as f:
            docdata = json.load(f)

        if not(docname in docdata):
            raise karDFM_DocNotFoundError(f"DocNotFoundError : No document found in the name '{docname}'")
        else:
            pass

        doctype = docdata[docname]["doctype"]

        if doctype == "json":
            with open(self.path + docname + ".json") as f:
                self.data = json.load(f)

        self.dfname = docname
        self.dftype = doctype

    def fetchdoclist(self):
        with open(self.docdatapath, "r") as f:
            return tuple(json.load(f).keys())
        
    def fetchdocdata(self):
        with open(self.docdatapath, "r") as f:
            return json.load(f)
        
    def savedoc(self):
        if self.dftype == "json":
            print(self.path + self.dfname + ".json")
            with open(self.path + self.dfname + ".json", "w") as f:
                json.dump(self.data, f, indent = 3)