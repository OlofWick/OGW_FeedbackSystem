import time
import socket
import requests
import json
import threading
import copy

######################################################################
class sensorReader (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ip = None

    def run(self):
        while self.ip is None :
            try:
                self.ip = socket.gethostbyname(self.name)
            except (socket.timeout, socket.gaierror, socket.herror) as e:
                print ("Sensor " + self.name +  ": IP address lookup error. Retrying...")
                print (e)
                time.sleep(30) # Sleep 30s if we couldn't find the host and then try again
            else:
                print("Sensor " + self.name +  " has IP address " + self.ip)

        while True:
            try:
                r = requests.get("http://" + self.ip)
            except Exception as e:
                print("Sensor " + self.name + " at IP " + self.ip + " not available. Retrying")
                print(e)
                time.sleep (10) # Sleep 10s and try again
            else:
                semaphore.acquire()
                routeDict[self.name] = r.json()
                print (self.name, r.status_code, sep=':')
                semaphore.release()
                time.sleep(15) # Poll every 15s

######################################################################
class displayUpdater (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        localDict = {}
        while True:
            semaphore.acquire()
            # Don't lock common data longer than necessary
            # Probably not needed but I do it for the style
            localDict = copy.deepcopy(routeDict)
            semaphore.release()

            for i in localDict.keys():
                for j in localDict[i].keys():
                    if "Rou" in j :
                        self.updateDisp(localDict[i]["Name"], j, localDict[i][j])
            time.sleep(5) # Update display every 5s

    def updateDisp(self, grp, route, state):
        print (grp, route, state)

######################################################################
# Global variables

semaphore = threading.Lock()
routeDict = {}
threads = []

######################################################################
# Main

threads.append(sensorReader(1, 'vxlgrp0-1.local'))
#threads.append(sensorReader(2, 'vxlgrp0-2.local'))
threads.append(sensorReader(3, 'vxlgrp0-3.local'))
#threads.append(sensorReader(4, 'vxlgrp0-4.local'))
threads.append(displayUpdater())

for t in threads:
   t.start()

for t in threads:
   t.join()

print ("Exiting ringen.py")
