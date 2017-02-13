import requests
r = requests.get("http://lundarallarna.se")
print (r.status_code)
print (r.headers)

