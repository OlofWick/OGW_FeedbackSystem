import time
import socket
import requests
import json

def query(name):
    ip = None
    while ip is None :
        try:
            ip = socket.gethostbyname(name)
        except (socket.timeout, socket.gaierror, socket.herror) as e:
            print ("Sensor " + name +  ": IP address lookup error. Retrying...")
            print (e)
            time.sleep(30) # Sleep 30s if we couldn't find the host and then try again
        else:
            print("Sensor " + name +  " has IP address " + ip)
            
    while True:
        try:
            r = requests.get("http://" + ip)
        except Exception as e:
            print("Sensor " + name + " at IP " + ip + " not available. Retrying")
            print(e)
            time.sleep (10) # Sleep 10s and try again
        else:
            print (r.status_code)
            print (r.json())
            print (r.json()['SW_Version'])
            time.sleep(15) # Poll every 15s
        
query('vxlgrp0-3.local')
