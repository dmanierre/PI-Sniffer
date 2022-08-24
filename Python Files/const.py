#Constants that will be used throughout the program

#Regex Patterns
MAC_PATTERN = "[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9][a-zA-Z0-9]"
ACTION_PATTERNS = {r"START_SCAN_\d\d_[0-9]+":"START_SCAN_TIME_COUNT", r"START_SCAN_DEFAULT_\d":"START_SCAN_DEFAULT_COUNT", r"^START_SCAN_\d\d$":"START_SCAN_TIME", r"^START_SCAN$":"START_SCAN_DEFAULT", "STOP_SCAN":"STOP_SCAN", "HELP":"HELP", "SHUTDOWN":"SHUTDOWN", "REBOOT":"REBOOT"}

#Message Text
HELPTEXT = "Commands:\n\tStart Scan \n\tStop Scan \n\tReboot \n\tTerminate"
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
TERMINATE = "TERMINATE"
HELP = "HELP"
REBOOT = "REBOOT"
UNKNOWN = "UNKNOWN"

#Misc
PROBE_REQUEST = "Probe Request"
PI_ID = "802.11 228"
DEFAULT_SCAN_TIME = "20"
CONTINUOUS = "CONTINUOUS"

