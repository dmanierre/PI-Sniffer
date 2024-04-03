import const
import user_settings
import mqtt_utils
import serial_utils
from time import sleep

if __name__ == '__main__':

    sleep(20)
    action = ""
    scanTime = const.DEFAULT_SCAN_TIME

    if user_settings.USEMQTT:
        mqtt_utils.startMQTTConnection()
    else:
        serial_utils.startSerialConnection()