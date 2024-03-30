import const
import helpers
import os
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from time import sleep
import paho.mqtt.client as paho
import json
import chardet

#Notify user of successful Meshtastic serial connection and subscribe to listener for Meshtastic packets
def startSerialConnection():
    interface.sendText(const.SCANNER_CONNECTED)

    #Subscribe to listener for Meshtastic packets
    pub.subscribe(onPacketReceive, "meshtastic.receive.text")

#Notify user of successful Meshtastic MQTT broker connection and subscribe to topic for Meshtastic packets
def startMQTTConnection():
    interface.sendText(const.SCANNER_CONNECTED)

    #Subscribe to listener for Meshtastic packets
    pub.subscribe(onPacketReceive, "meshtastic.receive.text")


#Handle incoming Meshtastic packets and convert to actions
def onPacketReceive(packet, interface):
    global action
    global scanTime
    packetActions = helpers.getActionFromPacket(packet)
    action = packetActions[0]
    scanTime = packetActions[1]

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
   


if __name__ == '__main__':
    action = ""
    scanTime = const.DEFAULT_SCAN_TIME

    if const.USEMQTT:
        startMQTTConnection()
    else:
        interface = meshtastic.serial_interface.SerialInterface()
        startSerialConnection()

    startScanner()