import json
import time

def combinemetadata(object docmetadata, bytes data) -> bytes:
    cdef bytes bdocmetadata, join

    bdocmetadata = json.dumps(docmetadata).encode()
    join = bdocmetadata + b"\n" + data

    return join



def extractmetadata(bytes bdata) -> object:
    cdef str sdata
    cdef object docmetadata
    cdef bytes data

    sdata = bdata.decode()
    docmetadata = json.loads(sdata.split("\n", 1)[0])
        
    return docmetadata



def removedocmetadata(str bakfpath) -> None:
    cdef bytes bdata, data
    cdef str sdata

    with open(bakfpath, "rb") as f:
        bdata = f.read()

    sdata = bdata.decode()
    data = sdata.split("\n", 1)[1].encode()

    with open(bakfpath, "wb") as f:
        f.write(data)



def createfull(str docname, str spath, str bakpath, object docmetadata) -> object:
    cdef bytes data, bdata
    cdef str ftimestamp

    with open(spath, "rb") as f:
        data = f.read()

    ftimestamp = time.strftime("%Y%m%d%H%M%S")
    bakname = docname + ftimestamp
    bakfpath = bakpath + "\\" + docname + "\\" + bakname + ".bak"

    docmetadata["backup"] = True
    docmetadata["backups"].append([bakname, bakfpath, ftimestamp])
    
    bdata = combinemetadata(docmetadata, data)

    with open(bakfpath, "wb") as f:
        f.write(bdata)

    return docmetadata



def loadfull(str path, str bakpath, object docmetadata, int n) -> None:
    cdef str bakfpath

    bakfpath = docmetadata["backups"][-n][1]

    with open(bakfpath, "rb") as f:
        bdata = f.read()

    with open(path, "wb") as f:
        f.write(bdata)