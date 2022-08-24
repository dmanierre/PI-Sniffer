import const
import helpers
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from time import sleep

#Notify user of successful Meshtastic connection and subscribe to listener for Meshtastic packets
def startConnection():
    interface.sendText(const.SCANNER_CONNECTED)

    #Subscribe to listener for Meshtastic packets
    pub.subscribe(onPacketReceive, "meshtastic.receive.text")

#Handle incoming Meshtastic packets and convert to actions
def onPacketReceive(packet, interface):
    global action
    global scanTime
    global scanRepetitions
    packetActions = helpers.getActionFromPacket(packet)
    action = packetActions[0]
    scanTime = packetActions[1]
    scanRepetitions = packetActions[2]

#Handles actions from users
def startScanner():
    global action
    global scanTime
    global scanRepetitions

    #While the user is not shutting down the program
    while action != const.TERMINATE:
        
        #Notify the user if they enter an unknown command
        if action == const.UNKNOWN:
            interface.sendText(const.UNKNOWNMESSAGE)
            action = ""
        
        #Run scan while action is Start
        while action == const.START:
            if(scanRepetitions != const.CONTINUOUS):
                for x in range(int(scanRepetitions)):
                    helpers.startScan(scanTime)
                    interface.sendText(helpers.parseScanResults())
                action = ""
                interface.sendText(const.SCAN_FINISHED)
            else:
                helpers.startScan(scanTime)
                interface.sendText(helpers.parseScanResults())
        
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
            sleep(2)
            interface.close()
            #OS command to reboot PI
    
    interface.sendText(const.SHUT_DOWN_MESSAGE)
    sleep(2)
    interface.close()
   


if __name__ == '__main__':
    interface = meshtastic.serial_interface.SerialInterface()
    action = ""
    scanTime = const.DEFAULT_SCAN_TIME
    scanRepetitions = ""
    startConnection()
    startScanner()