import requests
import datetime

url = 'http://series1-10306.local:5000/api/printer/tool?history=true'
headers = { 'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C' }

resp = requests.get(url, headers=headers)

if resp.status_code != 200:
    # This means something went wrong
    raise ApiError('BLAH')

r = resp.json()

for i in r['history']:
    print('Temp was: {} at Time: {}'.format(i['tool0']['actual'], datetime.datetime.fromtimestamp(i['time'])))
