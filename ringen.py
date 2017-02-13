import requests
r = requests.get("http://lundrallarna.se")
print (r.status_code)
print (r.headers)
print (r.content)
