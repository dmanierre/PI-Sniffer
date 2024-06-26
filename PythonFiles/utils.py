import const
import os
import re
import user_settings
from time import sleep

def startScan(scanTime):
    if user_settings.ENABLEPRINTS:
                print(f"Starting Scan")

    command = f"sudo tshark -i {user_settings.WIFIINTERFACE} -a duration:{scanTime} > scanResults.txt"
    os.system(command)

def parseScanResults():
    macAddresses = set()
    FileHandler = open("scanResults.txt","r")
    for line in FileHandler:
        if const.PROBE_REQUEST in line:
            if user_settings.PI_ID not in line:
                if re.search(const.MAC_PATTERN, line):
                    tempMac = re.search(const.MAC_PATTERN, line).group(0)
                    if tempMac not in macAddresses:
                        macAddresses.add(tempMac)
            
    FileHandler.close()
    if user_settings.ENABLEPRINTS:
                print(f"Devices Found: {len(macAddresses)}")
    return f"Devices Found: {len(macAddresses)}"


def startWithTime(packetText):
    action = const.START
    scanTime = packetText[1]

    packetActions = [action,scanTime]
    return packetActions

def startDefault(packetText):
    action = const.START
    scanTime = const.DEFAULT_SCAN_TIME

    packetActions = [action,scanTime]
    return packetActions

def stopScan(packetText):
    action = const.STOP
    scanTime = ""

    packetActions = [action,scanTime]
    return packetActions

def helpMessage(packetText):
    action = const.HELP
    scanTime = ""

    packetActions = [action,scanTime]
    return packetActions

def shutdownAction(packetText):
    action = const.SHUTDOWN
    scanTime = ""

    packetActions = [action,scanTime]
    return packetActions

def rebootAction(packetText):
    action = const.REBOOT
    scanTime = ""

    packetActions = [action,scanTime]
    return packetActions

ACTION_FUNCTIONS = {"SCAN_TIME":startWithTime, "SCAN":startDefault, "STOP_SCAN":stopScan, "HELP":helpMessage, "SHUTDOWN":shutdownAction, "REBOOT":rebootAction}
