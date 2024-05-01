#These are settings that will need to be configured individually when setting up the Pi

#-----------------------------------MQTT Settings-------------------------------------#

#Determines if the Meshtastic device will be connected via MQTT, if false then it will try to establish a serial connection (usb)
USEMQTT = True

#IP Address of Pi, make sure it is the IP of the hotspot interface
BROKERADDRESS = "10.42.0.1"

#Topic should match what is used on the MQTT section of the meshtastic device setup
TOPIC = "MESHSCANNER"

#This will be a string specific to each mestastic device. ex: !f7249454
MESHDEVICEID = "!f7249454"

#This is the Username created when setting up Mosquitto on the Pi
MQTTUSERNAME = "MeshDrone"

#This is the Password created when setting up Mosquitto on the Pi
MQTTPASSWORD = "MeshPass"
#------------------------------------------------------------------------------------#

#Decides if text will be printed out to the terminal (mostly for dev/debugging)
ENABLEPRINTS = True

#Wifi interface to scan with
WIFIINTERFACE = "wlan1"

#PI Packet Id
PI_ID = "802.11 228"

#Time before the scanner attempts to initaite connections
BOOT_TIME = 20

