import paho.mqtt.client as paho
from time import sleep
import os
import user_settings
import utils
import const
import mqtt_helper


#Notify user of successful Meshtastic MQTT broker connection and subscribe to topic for Meshtastic packets
def startMQTTScanner():
    global action
    global scanTime
    
    action = ""
    scanTime = const.DEFAULT_SCAN_TIME
    
    #Set client info and bind callbacks
    paho.Client.connected_flag = False
    client = paho.Client(paho.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username=user_settings.MQTTUSERNAME,password=user_settings.MQTTPASSWORD)
    client.on_connect = mqtt_helper.on_connect
    client.on_message = mqtt_helper.on_message
    client.on_publish = mqtt_helper.on_publish

    #Connect to the broker
    client.connect(user_settings.BROKERADDRESS, 1883, 60)
    client.loop_start()

    #Send successful connection message to the mesh
    client.publish(f"{user_settings.TOPIC}/2/json/mqtt", mqtt_helper.buildMqttMessage(const.SCANNER_CONNECTED))

    #Subscribe to the mesh device channel
    client.subscribe(f"{user_settings.TOPIC}/2/json/mqtt/{user_settings.MESHDEVICEID}",0)

    if user_settings.ENABLEPRINTS:
        print(f"Subscribed to channel {user_settings.TOPIC}/2/json/mqtt/{user_settings.MESHDEVICEID}")

    #While the user is not shutting down the program
    while action != const.SHUTDOWN:
        
        #Notify the user if they enter an unknown command
        if action == const.UNKNOWN:
            client.publish(f"{user_settings.TOPIC}/2/json/mqtt", mqtt_helper.buildMqttMessage(const.UNKNOWNMESSAGE))
            action = ""
        
        #Run scan while action is Start
        while action == const.START:
            utils.startScan(scanTime)
            client.publish(f"{user_settings.TOPIC}/2/json/mqtt", mqtt_helper.buildMqttMessage(utils.parseScanResults()))
            action = ""
        
        #Stop Scan and notify user when action is Stop
        while action == const.STOP:
            client.publish(f"{user_settings.TOPIC}/2/json/mqtt", mqtt_helper.buildMqttMessage(const.SCAN_STOPPED))
            action = ""

        #Send help text to user
        while action == const.HELP:
            client.publish(f"{user_settings.TOPIC}/2/json/mqtt", mqtt_helper.buildMqttMessage(const.HELPTEXT))
            action = ""
        
        #Reboot the Pi and relaunch the program
        if action == const.REBOOT:
            client.publish(f"{user_settings.TOPIC}/2/json/mqtt", mqtt_helper.buildMqttMessage(const.REBOOT_MESSAGE))
            sleep(5)
            client.disconnect()
            client.loop_stop()
            os.system("sudo reboot")
            
    client.publish(f"{user_settings.TOPIC}/2/json/mqtt", mqtt_helper.buildMqttMessage(const.SHUT_DOWN_MESSAGE))
    sleep(5)
    client.disconnect()
    client.loop_stop()
    os.system("sudo shutdown now")

