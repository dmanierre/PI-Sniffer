from asyncio import constants


import constants
import os
import re

def getActionFromPacket(packet):
    print("In Get Action")
    packetText = packet.get("decoded").get("text").upper().split("_")
    action = ""
    scanTime = constants.DEFAULT_SCAN_TIME
    if constants.SCAN in packetText:
        if constants.START in packetText:
            #Replace if check with regex to check if there is a valid number to set scan time to
            if len(packetText) == 3:
                scanTime = int(packetText[2])
            else:
                scanTime = constants.DEFAULT_SCAN_TIME
            action = constants.START
        elif constants.STOP in packetText:
            action = constants.STOP
    elif constants.TERMINATE in packetText:
        action = constants.TERMINATE
    elif constants.HELP in packetText:
        action = constants.HELP
    elif constants.REBOOT in packetText:
        action = constants.REBOOT
    else:
        action = constants.UNKNOWN
        
    packetActions = [action,scanTime]
    print(packetActions)
    return packetActions

def startScan(scanTime):
    command = f"sudo tshark -i mon1 -a duration:{scanTime} > scanResults.txt"
    os.system(command)

def parseScanResults():
    macAddresses = set()
    FileHandler = open("scanResults.txt","r")
    for line in FileHandler:
        if constants.PROBE_REQUEST in line:
            if constants.PI_ID not in line:
                if re.search(constants.MAC_PATTERN, line):
                    tempMac = re.search(constants.MAC_PATTERN, line).group(0)
                    if tempMac not in macAddresses:
                        macAddresses.add(tempMac)
            
    FileHandler.close()
    return f"Devices Found: {len(macAddresses)}"