import user_settings
import mqtt_scanner
import serial_scanner
from time import sleep

if __name__ == '__main__':

    if user_settings.ENABLEPRINTS:
        print("Waiting for system setup")
    #Give the system time to setup and let the Mesh device connect to the hotspot
    sleep(user_settings.BOOT_TIME)
    
    if user_settings.ENABLEPRINTS:
        print("Starting Scanner")

    if user_settings.USEMQTT:
        if user_settings.ENABLEPRINTS:
            print("Using MQTT connection")

        mqtt_scanner.startMQTTScanner()
    else:
        if user_settings.ENABLEPRINTS:
            print("Using Serial connection")

        serial_scanner.startSerialScanner()