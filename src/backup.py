import time, os, json  

def createfull(path,bpath,metadata):
    inv_path = path[::-1]
    dfname = inv_path.split(".",1)[1].split("\\",1)[0][::-1]

    timechar = time.strftime("%Y%m%d%H%M%S")
    bfname = dfname + timechar

    if not bpath[-1] in ("\\","/"):
        bpath = bpath + "\\"

    bfpath = bpath + dfname + "\\"
    os.makedirs(bfpath)

    with open(path,"rb") as f:
        data = f.read()
    
    record = [bfname, "full", bfpath]
    metadata["backups"].append(record)

    bdata = json.dumps(metadata).encode() + b"\n" + data

    path = bfpath + bfname + ".bak"
    with open(path, "wb") as f:
        f.write(bdata)

    return metadata

    

def loadfull(path,bpath,metadata,loadindex=-1):
    bfname = metadata["backups"][loadindex]
    dfname = bfname[:-14]
    if not bpath[-1] in ("\\","/"):
        bpath = bpath + "\\"

    with open(bpath + dfname + "\\" + bfname + ".bak", "rb") as f:
        data = f.read()

    metadata = json.loads(data.decode().split("\n")[0])
    data = data.decode().split("\n")[1:].encode()

    with open(path, "wb") as f:
        f.write(data)

    return metadata