import subprocess

listID = [123,124]
for getConID in listID:
    getDate = subprocess.getstatusoutput('date')
    stopLXC = subprocess.getstatusoutput('pct stop ' + str(getConID))
    print("Container " + str(getConID) + " was stopped")
    with open("stoppedLXCLog.txt" ,'a') as log_file:
        log_file.write(getDate[1] + " Container " + str(getConID) + " was stopped" + "\n")


# Change the list to input and give to the user decide what container he want to stop
# Set the inputs in a list
# If the user set "done" in the input continue the script and stop this containers
# write to the log file also the hostname of the container (check this in startLXC.py)