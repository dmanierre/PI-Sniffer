#Constants that will be used throughout the program

#Regex Patterns
MAC_PATTERN = "[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9][a-zA-Z0-9]"
ACTION_PATTERNS = {r"SCAN_\d\d$":"SCAN_TIME", "SCAN":"SCAN", "STOP_SCAN":"STOP_SCAN", "HELP":"HELP", "SHUTDOWN":"SHUTDOWN", "REBOOT":"REBOOT"}

#Message Text
HELPTEXT = "Commands:\n     Start_Scan \n     Start_Scan_** \n     Start_Scan_default_* \n     Start_Scan_**_* \n     Stop_Scan \n     Reboot \n     Shutdown \n\n** Represents scan duration input and * represents scan count input"
SCANNER_CONNECTED = "Scanner Connected"
UNKNOWNMESSAGE = "Unknown Command, type Help to view a list of commands."
REBOOT_MESSAGE = "Reboot request received. Restarting hardware"
SCAN_STOPPED = "Scan Stopped"
SHUT_DOWN_MESSAGE = "Shutting Down"
SCAN_FINISHED = "Scan Finished"

#Actions
SCAN = "SCAN"
START = "START"
STOP = "STOP"
SHUTDOWN = "SHUTDOWN"
HELP = "HELP"
REBOOT = "REBOOT"
UNKNOWN = "UNKNOWN"

#Misc
PROBE_REQUEST = "Probe Request"
PI_ID = "802.11 228"
DEFAULT_SCAN_TIME = "20"