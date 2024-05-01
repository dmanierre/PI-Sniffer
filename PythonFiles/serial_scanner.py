import meshtastic
import meshtastic.serial_interface
import const
import  utils
from pubsub import pub
from time import sleep
import os
import serial_helper

#Notify user of successful Meshtastic serial connection and subscribe to listener for Meshtastic packets
def startSerialScanner():
    global action
    global scanTime

    action = ""
    scanTime = const.DEFAULT_SCAN_TIME

    interface = meshtastic.serial_interface.SerialInterface()
    interface.sendText(const.SCANNER_CONNECTED)

    #Subscribe to listener for Meshtastic packets
    pub.subscribe(serial_helper.onPacketReceive, "meshtastic.receive.text")

    #While the user is not shutting down the program
    while action != const.SHUTDOWN:
        
        #Notify the user if they enter an unknown command
        if action == const.UNKNOWN:
            interface.sendText(const.UNKNOWNMESSAGE)
            action = ""
        
        #Run scan while action is Start
        while action == const.START:
            utils.startScan(scanTime)
            interface.sendText(utils.parseScanResults())
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

