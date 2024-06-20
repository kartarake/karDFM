import json
import pickle
import os

from errorlib import *

import security

kardfm_supports = [
    "json",
    "txt",
    "bin"
]

class kardfm:
    def __init__(self, dfmname, path="local") -> None:
        if path == "local":
            path = dfmname+'\\'
        os.makedirs(path, exist_ok=True)
        self.path = path

        os.makedirs(path + "kardfm_camp\\", exist_ok=True)
        with open(self.path + "kardfm_camp\\metadata.json","w") as f:
            json.dump({}, f)
        self.metadatapath = self.path + "kardfm_camp\\metadata.json"

        self.dfmname = dfmname
        self.data = None
        
        self.dfname = None
        self.dftype = None

    def createdoc(self, docname, doctype="json") -> None:
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

        elif doctype == "txt":
            docpath = self.path + docname + ".txt"
            with open(docpath, "w") as f:
                f.write("")
        
        elif doctype == "bin":
            docpath = self.path + docname + ".bin"
            with open(docpath, "wb") as f:
                pickle.dump(None, f)

        with open(self.path + "kardfm_camp\\metadata.json","r") as f:
            data = json.load(f)

        data[docname] = {"doctype":doctype,"encrypted":False}

        with open(self.path + "kardfm_camp\\metadata.json", 'w') as f:
            json.dump(data,f,indent=3)

        self.loaddoc(docname)

    def loaddoc(self, docname, key=None, return_value=False) -> None:
        if not (type(docname) == str):
            raise karDFM_TypeError(f"TypeError : {docname} passed in for docname.\nOnly string data type is accepted for docname arg.")
        else:
            pass

        with open(self.metadatapath,'r') as f:
            metadata = json.load(f)

        if not(docname in metadata):
            raise karDFM_DocNotFoundError(f"DocNotFoundError : No document found in the name '{docname}'")
        else:
            pass

        doctype = metadata[docname]["doctype"]

        if metadata[docname]["encrypted"] and not key:
            raise karDFM_KeyNotPassed(f"There was no key passed when requesting to load an encrypted file {docname}")

        elif metadata[docname]["encrypted"] and key:
            with open(self.path + docname + "." + doctype, "rb") as f:
                edata = f.read().decode()
            
            edata = edata.lstrip('"%karDFM-Encrypted%"\n')
            data = security.decrypt(edata, key).decode().strip('"')

        elif doctype == "json":
            with open(self.path + docname + ".json") as f:
                data = json.load(f)

        elif doctype == "txt":
            with open(self.path + docname + ".txt") as f:
                data = f.read()
        
        elif doctype == "bin":
            with open(self.path + docname + ".bin", "rb") as f:
                data = pickle.load(f)

        if not return_value:
            self.data = data        
            self.dfname = docname
            self.dftype = doctype
        else:
            return data

    def fetchdoclist(self):
        with open(self.metadatapath, "r") as f:
            return tuple(json.load(f).keys())
        
    def ifdocexist(self, docname):
        if docname in self.fetchdoclist() and docname in self.fetchmetadata():
            return True
        else:
            return False
        
    def fetchmetadata(self):
        with open(self.metadatapath, "r") as f:
            return json.load(f)
        
    def putmetadata(self,metadata):
        with open(self.metadatapath, "w") as f:
            json.dump(metadata,f,indent=3)
        
    def savedoc(self, key=None):
        metadata = self.fetchmetadata()
        if metadata[self.dfname]["encrypted"] and not key:
            raise karDFM_KeyNotPassed(f"There was no key passed when requesting to load an encrypted file {self.dfname}")
        
        elif metadata[self.dfname]["encrypted"] and key:
            edata = security.encrypt(self.data,key)
            with open(self.path + self.dfname + "." + self.dftype, "wb") as f:
                f.write(edata)

        elif self.dftype == "json":
            with open(self.path + self.dfname + ".json", "w") as f:
                json.dump(self.data, f, indent = 3)
        
        elif self.dftype == "txt":
            with open(self.path + self.dfname + ".txt", "w") as f:
                f.write(self.data)

        elif self.dftype == "bin":
            with open(self.path + self.dfname + ".bin", "wb") as f:
                pickle.dump(self.data, f)
    
    def renamedoc(self, oldname, newname):
        if not (type(oldname) == str and type(newname) == str):
            raise karDFM_TypeError("Only string data type is accepted for oldname & newname arg")
        
        if oldname == self.dfname:
            self.dfname = newname

        if not oldname in self.fetchdoclist():
            raise karDFM_DocNotFoundError(f"DocNotFoundError : The document {oldname} doesn't exist.")
        
        os.rename(self.path + oldname + "." + self.dftype, self.path + newname + "." + self.dftype)

    def deletedoc(self, docname):
        if not(docname in self.fetchdoclist()):
            karDFM_DocNotFoundError(f"Document {docname} was not found.")

        metadata = self.fetchmetadata()
        doctype = metadata[docname]["doctype"]
        
        if docname == self.dfname:
            self.dfname = None
            self.dftype = None
            self.data = None

        del metadata[docname]
        self.putmetadata(metadata)

        os.remove(self.path + docname + "." + doctype)

    def generate_key(self):
        return security.fetchkey()
    
    def lockdoc(self, docname, key):
        if not docname in self.fetchdoclist():
            raise karDFM_DocNotFoundError(f"Document with name {docname} was not found.")
        
        metadata = self.fetchmetadata()
        path = self.path + docname + "." + metadata[docname]["doctype"]

        with open(path, "rb") as f:
            data = f.read()
        
        header = '"%karDFM-Encrypted%"\n'
        edata = security.encrypt(data,key)

        with open(path, "wb") as f:
            f.write((header+edata).encode())

        metadata = self.fetchmetadata()
        metadata[docname]["encrypted"] = True
        self.putmetadata(metadata)

    def unlockdoc(self, docname, key):
        if not docname in self.fetchdoclist():
            raise karDFM_DocNotFoundError(f"Document with name {docname} was not found.")
        
        metadata = self.fetchmetadata()
        path = self.path + docname + "." + metadata[docname]["doctype"]

        with open(path,"rb") as f:
            data = f.read().decode()

        header = '"%karDFM-Encrypted%"\n'

        if data.startswith(header):
            data = data.lstrip(header)
            try:
                data = security.decrypt(data, key)
            except ValueError:
                raise karDFM_WrongKeyError("Wrong key has been passed (or) The encrypted data was damaged.")
            
            with open(path, "wb") as f:
                f.write(data)

            if docname == self.dfname:
                self.loaddoc(docname)
            
            metadata = self.fetchmetadata()
            metadata[docname]["encrypted"] = False
            self.putmetadata(metadata)
        
        else:
            raise karDFM_DocNotEncrypted(f"The document {docname} is not encrypted to be decrypted.")