import utils
import const
import re
import utils

#Handle incoming Meshtastic packets and convert to actions
def onPacketReceive(packet, interface):
    global action
    global scanTime
    packetActions = getActionFromSerialPacket(packet)
    action = packetActions[0]
    scanTime = packetActions[1]

def getActionFromSerialPacket(packet):
    packetText = packet.get("decoded").get("text").upper().split("_")
    for key in const.ACTION_PATTERNS:
        if re.search(key,packet.get("decoded").get("text").upper()):
            parser = utils.ACTION_FUNCTIONS.get(const.ACTION_PATTERNS.get(key))
            return parser(packetText)
    
    packetActions = [const.UNKNOWN,"",""]
    return packetActions