import meshtastic
import meshtastic.serial_interface
import const
import helpers
from pubsub import pub

#Notify user of successful Meshtastic serial connection and subscribe to listener for Meshtastic packets
def startSerialConnection():
    interface = meshtastic.serial_interface.SerialInterface()
    interface.sendText(const.SCANNER_CONNECTED)

    #Subscribe to listener for Meshtastic packets
    pub.subscribe(onPacketReceive, "meshtastic.receive.text")

#Handle incoming Meshtastic packets and convert to actions
def onPacketReceive(packet, interface):
    global action
    global scanTime
    packetActions = helpers.getActionFromSerialPacket(packet)
    action = packetActions[0]
    scanTime = packetActions[1]