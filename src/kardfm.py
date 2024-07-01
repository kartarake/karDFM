import json, pickle
import os

from errorlib import *

import backup
import security

class kardfm:
    """## This is the object of karDFM which contains various methods to aid in file handling.
    """

    def __init__(self, dfmname, path="local") -> None:
        """## The constructor method for the class to set up folder & metadata.

        ### Args:
            - `dfmname (str)`: The name of the DFM.
            - `path (str, optional)`: The path where the DFM folder should settle in. Defaults to "local".
        """ 

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

        self.supports = [
            "json",
            "txt",
            "bin"
        ]

        self.backuptypes = ["full"]



    def createdoc(self, docname, doctype="json") -> None:
        """## To create a document / file with passed unique name. If datatype is passed then takes up that datatype or it will be json data file.

        ### Args:
            - `docname (str)`: The name of the document.
            - `doctype (str, optional)`: The type of datafile. Defaults to "json".

        ### Raises:
            - `karDFM_TypeError`: Raises when one of the arg's data type is not correct.
            - `karDFM_TypeDefError`: Raises when file creation of unsupported data type is requested.
        """

        if not (type(docname) == str):
            raise karDFM_TypeError(f"TypeError : {docname} passed in for docname.\nOnly string data type is accepted for docname arg.")
        
        if not (doctype in self.supports):
            raise karDFM_TypeDefError(f"TypeDefError : {doctype} is not supported. \nOnly pass in document types which are supported by karDFM")

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

        data[docname] = {
            "doctype":doctype,
            "encrypted":False,
            "backup":False,
            "backup-type":None,
            "backups":[]
            }

        with open(self.path + "kardfm_camp\\metadata.json", 'w') as f:
            json.dump(data,f,indent=3)

        self.loaddoc(docname)


        
    def loaddoc(self, docname, key=None, return_value=False) -> None:
        """## This is to load the data from a document of DFM. 

        ### Args:
            - `docname (str)`: The name of the document you want to load.
            - `key (bytes, optional)`: The key that was used to encrypt the data. Defaults to None.
            - `return_value (bool, optional)`: If you want the data to be returned insted of loading it up in class's variable. Defaults to False.

        ### Raises:
            - `karDFM_TypeError`: Raises when one of the arg's data type is not correct.
            - `karDFM_DocNotFoundError`: Raises when the document name specified was not found.
            - `karDFM_KeyNotPassed`: Raises when the key is not passed when trying to load an encrypted file.

        ### Returns:
            - `data`: The data stored in that file if return_value arg is set to True.
        """        
        if not (type(docname) == str):
            raise karDFM_TypeError(f"TypeError : {docname} passed in for docname.\nOnly string data type is accepted for docname arg.")

        with open(self.metadatapath,'r') as f:
            metadata = json.load(f)

        if not(docname in metadata):
            raise karDFM_DocNotFoundError(f"DocNotFoundError : No document found in the name '{docname}'")

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
        """## To fetch all the names of the document created in DFM in the form of tuple.

        ### Returns:
            - `tuple`: The tuple containing names of document.
        """        
        with open(self.metadatapath, "r") as f:
            return tuple(json.load(f).keys())
        

        
    def ifdocexist(self, docname):
        """## To check if there is a document with passed in name in DFM.

        ### Args:
            - `docname (str)`: The name of the document.

        ### Returns:
            - `bool`: True if that document exists, False if not.
        """        
        if docname in self.fetchdoclist():
            return True
        else:
            return False
        

        
    def fetchmetadata(self):
        """## To fetch the metadata of all the files stored in DFM in the form of JSON / python dictionary.

        ### Returns:
            - `dict`: The metadata of all files.
        """        
        with open(self.metadatapath, "r") as f:
            return json.load(f)
        

        
    def putmetadata(self,metadata):
        """## To save the passed in data to metadata file.

        ### Args:
            - `metadata (dict)`: The metadata of all files.
        """
        with open(self.metadatapath, "w") as f:
            json.dump(metadata,f,indent=3)


        
    def savedoc(self, key=None):
        """## To save the data to disk from the class's variable.

        ### Args:
            - `key (bytes, optional)`: The key used for encryption of the file if it is encrypted file. Defaults to None.

        ### Raises:
            - `karDFM_KeyNotPassed`: If it was an encrypted file but key was not passed.
        """        
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
        """## To rename the document to someother name in which another document exists.

        ### Args:
            - `oldname (str)`: The current name of the document.
            - `newname (str)`: The replacement name.

        ### Raises:
            - `karDFM_TypeError`: Raises if any of the arg's data type is not correct.
            - `karDFM_DocNotFoundError`: Raises if the mentioned document was not found.
        """        
        if not (type(oldname) == str and type(newname) == str):
            raise karDFM_TypeError("Only string data type is accepted for oldname & newname arg")
        
        if oldname == self.dfname:
            self.dfname = newname

        if not oldname in self.fetchdoclist():
            raise karDFM_DocNotFoundError(f"DocNotFoundError : The document {oldname} doesn't exist.")
        
        os.rename(self.path + oldname + "." + self.dftype, self.path + newname + "." + self.dftype)



    def deletedoc(self, docname):
        """## To delete the document with the name passed in as arg from DFM.

        ### Args:
            - `docname (str)`: The name of the document.
        """        
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
        """## To generate a safe key and to return it. This can be used for encryption.

        ### Returns:
            - `bytes`: A 32 byte long key.
        """        
        return security.fetchkey()


    
    def lockdoc(self, docname, key):
        """## To lock the document by encrypting the data inside it.

        ### Args:
            - `docname (str)`: The name of document you want to encrypt.
            - `key (bytes)`: The key you want to use for encryption.

        ### Raises:
            - `karDFM_DocNotFoundError`: Raises if no document were to be found with passed in name.
        """   
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
        """## To unlock the document which has been encrypted back to normal.

        ### Args:
            - `docname (str)`: The name of the encrypted document.
            - `key (bytes)`: The key which has been used for encryption.

        ### Raises:
            - `karDFM_DocNotFoundError`: Raises if that document mentioned was not found.
            - `karDFM_WrongKeyError`: Raises if wrong key was passed or the encrypted data was damaged.
            - `karDFM_DocNotEncrypted`: Raises if the document passed was not encrypted to be unlocked.
        """        
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
        

        
    def createbackup(self, docname, butype, bupath):
        metadata = self.fetchmetadata()
        docmetadata = metadata[docname]

        spath = self.path + docname + "." + docmetadata["doctype"]

        if butype == "full":
            docmetadata = backup.createfull(spath, bupath, docmetadata)
            metadata.update({docname:docmetadata})
        
        self.putmetadata(metadata)



    def loadbackup(self, bakpath , docname, n):
        mfepaths = backup.listdir(bakpath + docname + "\\")
        mfepath  = mfepaths[-1]
        docmetadata = backup.extractmetadata(mfepath)

        path = self.path + docname + "." + docmetadata["doctype"]
        backup.loadfull(path, False, docmetadata, n)
        backup.injectmetadata(self.metadatapath, docname, docmetadata)