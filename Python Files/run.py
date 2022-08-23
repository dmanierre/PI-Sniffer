from argparse import Action
import constants
import helpers
import meshtastic
import meshtastic.serial_interface
from pubsub import pub

#Notify user of successful Meshtastic connection and subscribe to listener for Meshtastic packets
def startConnection():
    interface.sendText(constants.SCANNER_CONNECTED)

    #Subscribe to listener for Meshtastic packets
    pub.subscribe(onPacketReceive, "meshtastic.receive.text")

#Handle incoming Meshtastic packets and convert to actions
def onPacketReceive(packet, interface):
    print("Received Packet")
    global action
    global scanTime
    packetActions = helpers.getActionFromPacket(packet)
    action = packetActions[0]
    scanTime = packetActions[1]
    print(action)

#Handles actions from users
def startScanner():
    global action
    global scanTime

    #While the user is not shutting down the program
    while action != constants.TERMINATE:
        
        #Notify the user if they enter an unknown command
        if action == constants.UNKNOWN:
            print("Unknown")
            interface.sendText(constants.UNKNOWNMESSAGE)
            action = ""
        
        #Run scan while action is Start
        while action == constants.START:
            print("Start")
            helpers.startScan(scanTime)
            interface.sendText(helpers.parseScanResults())
        
        #Stop Scan and notify user when action is Stop
        while action == constants.STOP:
            print("Stop")
            interface.sendText(constants.SCAN_STOPPED)
            action = ""

        #Send help text to user
        while action == constants.HELP:
            interface.sendText(constants.HELPTEXT)
            action = ""
        
        #
        if action == constants.REBOOT:
            interface.sendText(constants.REBOOT_MESSAGE)
            interface.close()
            #OS command to reboot PI
    
    print("Terminate")
    interface.sendText(constants.SHUT_DOWN_MESSAGE)
    interface.close()
   


if __name__ == '__main__':
    interface = meshtastic.serial_interface.SerialInterface()
    action = ""
    scanTime = constants.DEFAULT_SCAN_TIME
    startConnection()
    startScanner()