import PythonFiles.utils as utils
import const
import json
import user_settings
import chardet
import re

def on_message(mosq, obj, msg):
    global action
    global scanTime

    packetActions = utils.getActionFromMQTTPacket(msg)
    action = packetActions[0]
    scanTime = packetActions[1]

    mosq.publish('pong', 'ack', 0)

def on_connect(client, userdata, flags, rc, properties):
    if rc==0:
        client.connected_flag = True
        if user_settings.ENABLEPRINTS:
            print("Connected to broker")
    else:
        if user_settings.ENABLEPRINTS:
            print("Unable to connect to broker")

def on_publish(mosq, obj, mid, reason_codes, properties):
    pass

def buildMqttMessage(message):
    messageBody = {
    "from":4146369620,
    "channel":0,
    "type":"sendtext",
    "payload": message
    }

    return json.dumps(messageBody)

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
                        parser = utils.ACTION_FUNCTIONS.get(const.ACTION_PATTERNS.get(key))
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