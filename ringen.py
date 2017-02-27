## This code only works if avahi is running on the Raspberry
# sudo apt-get update
# sudo apt-get install avahi-daemon
# sudo apt-get install libnss-mdns
# sudo insserv avahi-daemon
# sudo systemctl enable avahi-daemon

# Compile this and other python files to improve start time
# python3 -m py_compile myscript.py


######################################################################
import time
import socket
import requests
import json
import threading
import copy
import ringenDisp as disp

######################################################################
class sensorReader (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ip = None
        self.connected = False
        self.keepOn = True

    def run(self):
        while (self.ip is None) and self.keepOn:
            try:
                self.ip = socket.gethostbyname(self.name)
            except (socket.timeout, socket.gaierror, socket.herror) as e:
                print ("Sensor " + self.name +  ": IP address lookup error. Retrying...")
                print (e)
                time.sleep(5) # Sleep 10s if we couldn't find the host and then try again
            else:
                print("Sensor " + self.name +  " has IP address " + self.ip)

        while self.keepOn:
            try:
                r = requests.get("http://" + self.ip)
            except Exception as e:
                print("Sensor " + self.name + " at IP " + self.ip + " not available. Retrying")
                print(e)
                self.connected = False
                time.sleep (5) # Sleep 10s and try again
            else:
                self.connected = True
                semaphore.acquire()
                routeDict[self.name] = r.json()
                semaphore.release()
                time.sleep(5) # Poll every 10s
        print("Sensor thread ", self.name, " terminated")

    def stop(self):
        self.keepOn = False

    def isConnected(self):
        return self.connected

    def getThreadId(self):
        return self.threadID


######################################################################
def updateDisp():
    root = win.getRoot()
    routes = win.getRoutes()
    lables = win.getStatusLbls()

    semaphore.acquire()
    # Don't lock common data longer than necessary
    # Probably not needed but I do it for the style
    localDict = copy.deepcopy(routeDict)
    semaphore.release()
    
    for grp in localDict.keys():
        if "vxl" in grp:
            for rou in localDict[grp].keys():
                if "Rou" in rou :
                    #Convert last character into integers
                    tmp = localDict[grp]["Name"]
                    g = int(tmp[-1])
                    r = int(rou[-1])
                    if localDict[grp][rou]:
                        routes.free(g,r)
                    else:
                        routes.blocked(g,r)

    for i in range(len(sensors)):
        # isConnected should be atiómic so no need for a semaphore
        if sensors[i].isConnected():
            lables[i].setOk()
        else:
            lables[i].setProblem()
            routes.unknown(i+1)            
    # Call again in 10 seconds
    root.after(10000, updateDisp)
                    

######################################################################
# Global variables

semaphore = threading.Lock()
routeDict = {}
threads = []
sensors = []

######################################################################
# Main
if __name__ == '__main__':

    sensors = [sensorReader(1, 'vxlgrp0-1.local'), \
               sensorReader(2, 'vxlgrp0-2.local'), \
               sensorReader(3, 'vxlgrp0-3.local'), \
               sensorReader(4, 'vxlgrp0-4.local')]

    for s in sensors:
       s.start()

    win = disp.layoutWindow("Ringens växellägen")

    # I would have hoped to keep this file free from Tkinter stuff but
    # Tkinter must run in the main loop so it wasn't possible
    #
    # Register a function that will be called regularly and start mainloop
    win.getRoot().after(10000, updateDisp)
    win.getRoot().mainloop()


    # We have exited the mainloop and it is time to close all threads
    # Send a stop signal to all threads
    for s in sensors:
       s.stop()
    # Wait for all threads to complete
    for s in sensors:
        s.join()
    print ("Exiting Main Thread")
    
