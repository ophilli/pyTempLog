import logging
import requests
import configparser
import pymysql.cursors
from datetime import datetime

logging.basicConfig(filename='temp.log', level=logging.WARNING)

api_tool = '/api/printer/tool?history=true'
api_bed = '/api/printer/bed?history=true'

sql_tool = """INSERT IGNORE INTO `ext_Temp` (`Temp_Actual`, `Temp_Target`, `Mach_Key`, `Time`) VALUES (%s, %s, %s, %s)"""
sql_bed = """INSERT IGNORE INTO `bed_Temp` (`Temp_Actual`, `Temp_Target`, `Mach_Key`, `Time`) VALUES(%s, %s, %s, %s)"""

hosts = [
	{'url' : 'http://series1-10156.local:5000', 'headers' : {'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C'}},
	{'url' : 'http://series1-10306.local:5000', 'headers' : {'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C'}},
	{'url' : 'http://series1-10307.local:5000', 'headers' : {'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C'}},
	{'url' : 'http://series1-10308.local:5000', 'headers' : {'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C'}},
	{'url' : 'http://series1-10309.local:5000', 'headers' : {'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C'}},
	{'url' : 'http://series1-10310.local:5000', 'headers' : {'X-Api-Key' : '7AA24AC7430A43ABAEA065C83458270C'}},
	{'url' : 'http://octopi.local', 'headers' : {'X-Api-Key' : '034769AFEB794CA5AC2E19D36DD89893'}}	
    ]

config = configparser.RawConfigParser()
config.read('secrets.cfg')

connection = pymysql.connect(host=config.get('_sql', 'hostname'),
				user=config.get('_sql', 'username'),
				password=config.get('_sql', 'password'),
				db=config.get('_sql', 'database')
			)
try:
	with connection.cursor() as cursor:
		for i in hosts:
			r_tool = requests.get(i['url'] + api_tool, headers=i['headers'])
			r_bed = requests.get(i['url'] + api_bed, headers=i['headers'])

			if r_tool.status_code != 200:
				logging.error(r_tool.status_code, datetime.now())
			if r_bed.status_code != 200:
				logging.error(r_bed.status_code, datetime.now())

			j_tool = r_tool.json()
			j_bed = r_bed.json()

			for j in j_tool['history']:
				d_tool = (j['tool0']['actual'], j['tool0']['target'], hosts.index(i), datetime.fromtimestamp(j['time']))
				cursor.execute(sql_tool, d_tool)

			for j in j_bed['history']:
				d_bed = (j['bed']['actual'], j['bed']['target'], hosts.index(i), datetime.fromtimestamp(j['time']))
				cursor.execute(sql_bed, d_bed)

			connection.commit()

finally:
	connection.close()

	logging.warning('Everything looks good at %s', datetime.now())
