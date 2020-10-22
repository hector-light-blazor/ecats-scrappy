import win32api, shutil

# MODULE: Get all hard drives available on computer
def getAllDrives():
    return [d for d in
            win32api.GetLogicalDriveStrings().rstrip('\0').split('\0')] 

# MODULE: From the list of drives which is the biggest size
def getBigDrive(drives):
    drive = {"total" : 0, "letter" : ''};
    for hd in drives:
        byteInfo = shutil.disk_usage(hd)
        freeByte = byteInfo[2]
        if freeByte > drive['total']:
            drive['total']  = freeByte
            drive['letter'] = hd
    return drive