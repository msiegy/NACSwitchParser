""" Iterate configuration files in a directory to return a list of interfaces
    that contain relevant children statements. From this list generate
    configuration files that include NAC changes.
"""

import os
from ciscoconfparse import CiscoConfParse

# Set config directories for existing and new output
dir = 'configs'
changes = 'nac-configs'

# Iterate through each file in the config directory
for filename in os.listdir('configs'):
    file = 'configs/'+filename
    outFile = open(changes+'/'+filename+'.delta', 'w')
    # Parse the config file into objects
    parse = CiscoConfParse(file, syntax='ios')
    interfaces = []

    SWversion = parse.re_match_iter_typed(r'^version\s(\S+)', default='no version')
    print('SW Version: ' + SWversion)

    # Iterate over all the interface objects
    for intf_obj in parse.find_objects('^interface'):

        has_switchport_access = intf_obj.has_child_with(r'switchport mode access')
        has_shutdown = intf_obj.has_child_with(r'shutdown')
        has_netdescript = intf_obj.has_child_with(r'description.*(router|switch|uplink|circuit).*')

        if (has_switchport_access or has_shutdown) and not has_netdescript:
            interfaces.append(intf_obj.text)
            intf_obj.append_to_family(' description **This Port Has Been NAC Enabled**')
            outFile.write(intf_obj.text)
            outFile.write('\n description **This Port Has Been NAC Enabled**\n')

    #Print interfaces which meet the child critera - for debugging
    print(*interfaces, sep = ', ')
    #Close the new configuration file that only contains NAC additions
    outFile.close()
    #Write new file that contains complete config, including old and new lines
    parse.save_as(changes+'/'+filename+'.new')

### TODO
### - Check Version, HW, etc
###  - Exclude ports with: existing nac config?
###  - Include ports with: portfast?
###  - external pre and post change valdiation (Up/Down status, arp tables, etc)
