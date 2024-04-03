import const
import user_settings
import os
import re
import chardet
import json
from time import sleep

#Handles actions from users
def startScanner():
    global action
    global scanTime

    #While the user is not shutting down the program
    while action != const.SHUTDOWN:
        
        #Notify the user if they enter an unknown command
        if action == const.UNKNOWN:
            interface.sendText(const.UNKNOWNMESSAGE)
            action = ""
        
        #Run scan while action is Start
        while action == const.START:
            helpers.startScan(scanTime)
            interface.sendText(helpers.parseScanResults())
            action = ""
        
        #Stop Scan and notify user when action is Stop
        while action == const.STOP:
            interface.sendText(const.SCAN_STOPPED)
            action = ""

        #Send help text to user
        while action == const.HELP:
            interface.sendText(const.HELPTEXT)
            action = ""
        
        #Reboot the Pi and relaunch the program
        if action == const.REBOOT:
            interface.sendText(const.REBOOT_MESSAGE)
            sleep(5)
            interface.close()
            os.system("sudo reboot")
            
    
    interface.sendText(const.SHUT_DOWN_MESSAGE)
    sleep(5)
    interface.close()
    os.system("sudo shutdown now")

def getActionFromSerialPacket(packet):
    packetText = packet.get("decoded").get("text").upper().split("_")
    for key in const.ACTION_PATTERNS:
        if re.search(key,packet.get("decoded").get("text").upper()):
            parser = ACTION_FUNCTIONS.get(const.ACTION_PATTERNS.get(key))
            return parser(packetText)
    
    packetActions = [const.UNKNOWN,"",""]
    return packetActions

def getActionFromMQTTPacket(msg):
    encoding = chardet.detect(msg.payload)['encoding']
    dataStr = msg.payload.decode(encoding)

    if dataStr:
        data = json.loads(msg.payload)
        if "payload" in data.keys():
            if "text" in data["payload"].keys():
                message = data['payload']['text']
                if user_settings.ENABLEPRINTS:
                    print(f"Message received: {message}")
                packetText = message.upper().split("_")
                for key in const.ACTION_PATTERNS:
                    if re.search(key,message.upper()):
                        parser = ACTION_FUNCTIONS.get(const.ACTION_PATTERNS.get(key))
                        return parser(packetText)

    else:
        if user_settings.ENABLEPRINTS:
            print("Empty message recieved")
        packetActions = [const.UNKNOWN,"",""]
        return packetActions    
    
    if user_settings.ENABLEPRINTS:
        print("No matching command found")

    packetActions = [const.UNKNOWN,"",""]
    return packetActions 

def startScan(scanTime):
    command = f"sudo tshark -i {const.WIFIINTERFACE} -a duration:{scanTime} > scanResults.txt"
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

def buildMqttMessage(message):
    messageBody = {
    "from":4146369620,
    "channel":0,
    "type":"sendtext",
    "payload": message
    }

    return json.dumps(messageBody)


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

#Update help text
#handle single digit scan times and double digit scan counts
