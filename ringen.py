import time
import socket
import requests
import json
import threading

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
                print (r.status_code)
                print (r.json())
                print (r.json()['SW_Version'])
                semaphore.release()
                time.sleep(15) # Poll every 15s

semaphore = threading.Lock()

threads = []

grp1Reader = sensorReader(1, 'vxlgrp0-1.local')
threads.append(grp1Reader)
grp3Reader = sensorReader(3, 'vxlgrp0-3.local')
threads.append(grp3Reader)

for t in threads:
   t.start()

for t in threads:
   t.join()

print ("Exiting ringen.py")
