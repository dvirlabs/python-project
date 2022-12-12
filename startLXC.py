from netmiko import ConnectHandler
import re
import subprocess
from pprint import pprint

linux = {
    'device_type': 'linux',
    'ip': '192.168.1.120',
    'username': 'root',
    'password': 'dvir4210200H',
    'port': 22,
    'verbose': True
}
# Connect to the Linux Server
connection = ConnectHandler(**linux)
output = connection.send_command('sudo pct list | tail -n +2') # Get the list of the containers with name and status
pattern = "\d{3}" # Extract the ID of the containers
getConID = re.findall(pattern , output) # List of the containers ID
connection.disconnect()


id2hostname = subprocess.getstatusoutput("""pct list | awk '{ print $1 ":" $3 }'""")
temp = id2hostname[1].split('\n')
getConID = {}
for line in temp:
    sp = line.split(':')
    if sp and len(sp) == 2 and re.search('^[0-9]+$', sp[0]):
        getConID[ sp[0].strip() ] = sp[1].strip()

for container in getConID.keys(): # Var that get the value of each container in the list
    getDate = subprocess.getstatusoutput('date')
    execCommand = subprocess.getstatusoutput('sudo pct status ' + container) # Set command on each contaienr
    # getHostname = subprocess.getstatusoutput("pct list | awk '{ print $3 }'")
    if (execCommand[1] == "status: stopped"):        
        print('Container ' + getConID[container] + ' ' + container + ' ' + 'will be start now...', end='')
        startCon = subprocess.getstatusoutput('pct start ' + container) # Start the container if the status is "stopped"
        print('done!')
        with open("startedLXCLog.txt" ,'a') as log_file:
            log_file.write(getDate[1] + " Container " + getConID[container] + " was started" + "\n")
    else:
        print ("Container " + getConID[container] + ' ' + container + ' ' + re.sub("status:" , "is:" , execCommand[1])) # Print the status of the container


