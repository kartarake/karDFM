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
    
    path = bfpath + bfname + ".bak"
    record = [bfname, "full", path]
    metadata["backups"].append(record)

    bdata = json.dumps(metadata).encode() + b"\n" + data

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



def extractmetadata(path, removefromfile=True):
    with open(path, 'rb') as f:
        data = f.read().decode()

    metadata = json.loads(data.split("\n")[0])
    if removefromfile:
        data = data.split("\n")[1:]
        data = "".join(data).encode()
        
        with open(path, 'wb') as f:
            f.write(data)
    
    return metadata



def injectmetadata(path, docname, data):
    with open(path, "r") as f:
        sdata = json.load(f)

    sdata.update({docname:data})

    with open(path, "w") as f:
        json.dump(sdata, f, indent=3)



def loadfull(path, bfpath, docmetadata, n):
    if not bfpath:
        bfpath = docmetadata["backups"][-n][2]

    with open(bfpath, "rb") as f:
        data = f.read()
    
    with open(path, "wb") as f:
        f.write(data)



def listdir(path):
    paths = os.listdir(path)
    paths = [path + i for i in paths]
    paths.sort()
    return paths