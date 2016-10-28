import logging
import requests
import datetime
import mysql.connector

logging.basicConfig(filename='temp.log', level=logging.INFO)

api = '/api/printer/tool?history=true'
add_ext = """INSERT INTO `ophilli`.`Temperatures` (`Temp_Actual`, `Temp_Target`, `Serial_Number`, `Time`) VALUES (%s, %s, %s, %s)"""

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


url = 'http://series1-10306.local:5000/api/printer/tool?history=true'
headers = { 'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C' }

hosts = {
	10156, 
	10306, 
	10307, 
	10308, 
	10309, 
	10310
    }

for i in hosts:
	resp = requests.get('http://series1-' + str(i) + '.local:5000' + api, headers=headers)

	if resp.status_code != 200:
	    # This means something went wrong
	    raise ApiError('BLAH')

	r = resp.json()

	emp_no = 0

	for j in r['history']:
	    data_temp = (j['tool0']['actual'], j['tool0']['target'], i, datetime.datetime.fromtimestamp(j['time']))
	    # print('Temp was: {} at Time: {}'.format(i['tool0']['actual'], datetime.datetime.fromtimestamp(i['time'])))
	    cursor.execute(add_ext, data_temp)

cnx.commit()

cursor.close()
cnx.close()

logging.info('Everything looks good at %s', datetime.datetime.now())
