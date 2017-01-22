import logging
import requests
import json

api = '/api/printer/tool'

headersi = { 'Content-Type': 'application/json',
	    'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C' }
datai = { "command" : "target",
	  "targets" : { "tool0": 220 }
	}

hosts = [
	10306,
	10307, 
	10308, 
	10309, 
	10310,
	10156
    ]

for i in hosts:
	resp = requests.post('http://series1-' + str(i) + '.local:5000' + api, data=json.dumps(datai), headers=headersi)
	print(resp.status_code)
