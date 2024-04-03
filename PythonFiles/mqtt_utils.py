import paho.mqtt.client as paho
import json
import user_settings
import helpers
import const


#Notify user of successful Meshtastic MQTT broker connection and subscribe to topic for Meshtastic packets
def startMQTTConnection():
    global action
    global scanTime
    
    #Set client info and bind callbacks
    paho.Client.connected_flag = False
    client = paho.Client(paho.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username=user_settings.MQTTUSERNAME,password=user_settings.MQTTPASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    #Connect to the broker
    client.connect(user_settings.BROKERADDRESS, 1883, 60)
    client.loop_start()

    #Send successful connection message to the mesh
    client.publish(f"{user_settings.TOPIC}/2/json/mqtt", helpers.buildMqttMessage(const.SCANNER_CONNECTED))

    #Subscribe to the mesh device channel
    client.subscribe(f"{user_settings.TOPIC}/2/json/mqtt/{user_settings.MESHDEVICEID}",0)

    if user_settings.ENABLEPRINTS:
        print(f"Subscribed to channel {user_settings.TOPIC}/2/json/mqtt")

    #While the user is not shutting down the program
    while action != const.SHUTDOWN:
        
        #Notify the user if they enter an unknown command
        if action == const.UNKNOWN:
            client.publish(f"{user_settings.TOPIC}/2/json/mqtt", helpers.buildMqttMessage(const.UNKNOWNMESSAGE))
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

    helpers.startScanner()

def on_message(mosq, obj, msg):
    global action
    global scanTime

    packetActions = helpers.getActionFromMQTTPacket(msg)
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