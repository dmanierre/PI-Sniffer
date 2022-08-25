import const
import os
import re

def getActionFromPacket(packet):
    packetText = packet.get("decoded").get("text").upper().split("_")
    for key in const.ACTION_PATTERNS:
        if re.search(key,packet.get("decoded").get("text").upper()):
            parser = ACTION_FUNCTIONS.get(const.ACTION_PATTERNS.get(key))
            return parser(packetText)
    
    packetActions = [const.UNKNOWN,"",""]
    return packetActions

def startScan(scanTime):
    command = f"sudo tshark -i mon1 -a duration:{scanTime} > scanResults.txt"
    os.system(command)

def parseScanResults():
    macAddresses = set()
    FileHandler = open("scanResults.txt","r")
    for line in FileHandler:
        if const.PROBE_REQUEST in line:
            if const.PI_ID not in line:
                if re.search(const.MAC_PATTERN, line):
                    tempMac = re.search(const.MAC_PATTERN, line).group(0)
                    if tempMac not in macAddresses:
                        macAddresses.add(tempMac)
            
    FileHandler.close()
    return f"Devices Found: {len(macAddresses)}"

def startWithTimeAndCount(packetText):
    action = const.START
    scanTime = packetText[2]
    scanRepetitions = packetText[3]

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

def startWithCount(packetText):
    action = const.START
    scanTime = const.DEFAULT_SCAN_TIME
    scanRepetitions = packetText[3]

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

def startWithTime(packetText):
    action = const.START
    scanTime = packetText[2]
    scanRepetitions = const.CONTINUOUS

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

def startDefault(packetText):
    action = const.START
    scanTime = const.DEFAULT_SCAN_TIME
    scanRepetitions = const.CONTINUOUS

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

def stopScan(packetText):
    action = const.STOP
    scanTime = ""
    scanRepetitions = ""

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

def helpMessage(packetText):
    action = const.HELP
    scanTime = ""
    scanRepetitions = ""

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

def shutdownAction(packetText):
    action = const.SHUTDOWN
    scanTime = ""
    scanRepetitions = ""

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

def rebootAction(packetText):
    action = const.REBOOT
    scanTime = ""
    scanRepetitions = ""

    packetActions = [action,scanTime,scanRepetitions]
    return packetActions

ACTION_FUNCTIONS = {"START_SCAN_TIME_COUNT":startWithTimeAndCount, "START_SCAN_DEFAULT_COUNT":startWithCount, "START_SCAN_TIME":startWithTime, "START_SCAN_DEFAULT":startDefault, "STOP_SCAN":stopScan, "HELP":helpMessage, "SHUTDOWN":shutdownAction, "REBOOT":rebootAction}

#Update help text
#handle single digit scan times and double digit scan counts
