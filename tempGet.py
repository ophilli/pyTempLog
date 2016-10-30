import logging
import requests
import datetime
import mysql.connector

logging.basicConfig(filename='temp.log', level=logging.INFO)

api_ext = '/api/printer/tool?history=true'
api_bed = '/api/printer/bed?history=true'

add_ext = """INSERT IGNORE INTO `ophilli`.`ext_Temp` (`Temp_Actual`, `Temp_Target`, `Mach_Key`, `Time`) VALUES (%s, %s, %s, %s)"""
add_bed = """INSERT IGNORE INTO `ophilli`.`bed_Temp` (`Temp_Actual`, `Temp_Target`, `Mach_Key`, `Time`) VALUES (%s, %s, %s, %s)"""

try:
    cnx = mysql.connector.connect(user='ophilli', password='****', host='sbxmysql.clemson.edu', database='ophilli')

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    logging.warning("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    logging.warning("Database does not exist")
  else:
    logging.warning(err)

cursor = cnx.cursor()

headers = { 'X-Api-Key' : 'E09D1F4FA1304F05A9DC9E6283D23674' }

respExt = requests.get('http://octopi3.local' + api_ext, headers=headers)
respBed = requests.get('http://octopi3.local' + api_bed, headers=headers)

if respExt.status_code != 200:
    raise ApiError('EXT ERROR')
if respBed.status_code != 200:
    raise ApiError('BED ERROR')

rExt = respExt.json()
rBed = respBed.json()

for j in rExt['history']:
    data_ext = (j['tool0']['actual'], j['tool0']['target'], 6, datetime.datetime.fromtimestamp(j['time']))
    cursor.execute(add_ext, data_ext)

for k in rBed['history']:
    data_bed = (k['bed']['actual'], k['bed']['target'], 6, datetime.datetime.fromtimestamp(k['time']))
    cursor.execute(add_bed, data_bed)



headers = { 'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C' }

hosts = [
	10156, 
	10306, 
	10307, 
	10308, 
	10309, 
	10310
    ]

for i in hosts:
	respExt = requests.get('http://series1-' + str(i) + '.local:5000' + api_ext, headers=headers)
	respBed = requests.get('http://series1-' + str(i) + '.local:5000' + api_bed, headers=headers)
	
	if respExt.status_code != 200:
	    raise ApiError('EXT ERROR')
	if respBed.status_code != 200:
	    raise ApiError('BED ERROR')

	rExt = respExt.json()
	rBed = respBed.json()

	for j in rExt['history']:
	    data_ext = (j['tool0']['actual'], j['tool0']['target'], hosts.index(i), datetime.datetime.fromtimestamp(j['time']))
	    cursor.execute(add_ext, data_ext)

        for k in rBed['history']:
            data_bed = (k['bed']['actual'], k['bed']['target'], hosts.index(i), datetime.datetime.fromtimestamp(k['time']))
            cursor.execute(add_bed, data_bed)

cnx.commit()

cursor.close()
cnx.close()

logging.info('Everything looks good at %s', datetime.datetime.now())
