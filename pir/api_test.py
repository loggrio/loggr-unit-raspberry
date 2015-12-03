import requests
import json
from time import time

PICS_PATH = 'Logo.png'
CONTAINERS_URL = 'http://0.0.0.0:3000/api/containers/'

# create container
container_name = str(int(time()))
payload = {'name': container_name}
headers = {'Content-Type': 'application/json'}
print 'create container ' + container_name
print 'result code: ' + str(requests.post(CONTAINERS_URL,
                                          data=json.dumps(payload),
                                          headers=headers))

# send file to container
filename = str(int(time())) + '.jpg'
files = {'file': (filename, open(PICS_PATH, 'rb'))}
PICS_URL = CONTAINERS_URL + container_name + '/upload'
print 'upload file ' + filename
print 'result code: ' + str(requests.post(PICS_URL, files=files))
