# NACSwitchParser
Switch configuration parser that leverages the python library ciscoconfparse for identifying where to apply appropriate NAC configs


iosparser.py 
""" Iterates Cisco IOS configuration files in a directory to return a list of interfaces
    that contain relevant children statements. From this list generate
    configuration files that include NAC changes. One file for complete configuration and one file for new changes only.
"""

