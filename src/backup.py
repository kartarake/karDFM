import time, os

def createfull(path,bpath,metadata):
    inv_path = path[::-1]
    dfname = inv_path.split(".",1)[1].split("\\",1)[0][::-1]

    timechar = time.strftime("%Y.%m.%d %H:%M:%S")
    bfname = dfname + timechar

    if not bpath[-1] in ("\\","/"):
        bpath = bpath + "\\"

    bfpath = bpath + dfname + "\\"
    os.makedirs(bfpath)

    with open(path,"rb") as f:
        data = f.read()

    with open(bfpath + bfname + ".bak", "wb") as f:
        f.write(data)

    metadata["backups"].append(bfname)

    

def loadfull(path,bpath,metadata,loadindex=-1):
    bfname = metadata["backups"][loadindex]
    if not bpath[-1] in ("\\","/"):
        bpath = bpath + "\\"

    with open(bpath + bfname + ".bak", "rb") as f:
        data = f.read()

    with open(path, "wb") as f:
        f.write(data)