import json

def combinemetadata(object docmetadata, bytes data) -> bytes:
    cdef bytes bdocmetadata, join

    bdocmetadata = json.dumps(docmetadata).encode()
    join = bdocmetadata + b"\n" + data

    return join



def extractmetadata(bytes bdata) -> object:
    cdef str sdata
    cdef object docmetadata

    sdata = bdata.decode()
    docmetadata = json.loads(sdata.split("\n")[0])

    return docmetadata 