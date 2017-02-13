import requests
import json


r = requests.get("http://vxlgrp0-1.local")
print (r.status_code)
print (r.json())
print (json.dumps(r.json()))
test = json.loads(json.dumps(r.json()))
print (test)
print (test['Name'])



