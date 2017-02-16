import time
import socket
import requests
import json

def query(name):
    ip = socket.gethostbyname(name)
    while True:
        r = requests.get("http://" + ip)
        print (r.status_code)
        print (r.json())
        print (r.json()['SW_Version'])
        time.sleep(30)

query('vxlgrp0-3.local')
