import json
import os

from errorlib import *

kardfm_supports = [
    "json"
]

class kardfm:
    def __init__(self, dfmname, path) -> None:
        if path == "local":
            path = dfmname+'\\'
        os.makedirs(path, exist_ok=True)
        self.path = path

        os.makedirs(path + "kardfm_camp\\", exist_ok=True)
        with open(self.path + "kardfm_camp\\docdata.json","w") as f:
            json.dump({}, f)

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

        self.dfmname = docname
        self.dftype = doctype

        with open(self.path + "kardfm_camp\\docdata.json","r") as f:
            data = json.load(f)

        data[docname] = {"doctype":doctype}

        with open(self.path + "kardfm_camp\\docdata.json", 'w') as f:
            json.dump(data,f,indent=3)