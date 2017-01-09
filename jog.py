import logging
import requests
import json

api = '/api/printer/printhead'

headersi = { 'Content-Type': 'application/json',
	    'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C' }
datai = { "command" : "jog",
	  "x": 152,
	  "y": -152,
	  "z": 0}

hosts = [
	'repair',
	10307, 
	10308, 
	10309, 
	10310
    ]

for i in hosts:
	resp = requests.post('http://series1-' + str(i) + '.local:5000' + api, data=json.dumps(datai), headers=headersi)
	print(resp.status_code)
