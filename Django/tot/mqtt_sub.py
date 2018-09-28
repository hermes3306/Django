import paho.mqtt.client as mqtt
import logging
import json
import pymysql
import time

def on_connect(client, userdata, rc):
	logger.info("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
	try:
		data = json.loads(msg.payload.decode('utf8'))
		logger.info(data)
		db = pymysql.connect(
			host='localhost',
			port=3306,
			user='laravel',
			passwd='laravel',
			db='laravel',
			charset='utf8')
		curs = db.cursor()
		sql1="select (1) from tot_tot where yymmdd like %s and accnt like %s"
		sql2="delete from tot_tot where yymmdd like %s and  accnt like %s"
		sql3 = "insert into tot_tot(accnt,money,yymmdd) values(%s,%s,%s)"
		for x in range(0, len(data)):
			isexist = curs.execute(sql1, (data[x]["yymmdd"], data[x]["accnt"]))
			if isexist:
				curs.execute(sql2,(data[x]["yymmdd"], data[x]["accnt"]))
			curs.execute(sql3,(data[x]["accnt"], data[x]["money"], data[x]["yymmdd"]))
		db.commit()
		db.close()
	except Exception as e:
		logger.info(str(e))

with open('tot.json','r') as f:
    conf = json.load(f)

mqtt_server = conf['MQTT']['SERVER']
mqtt_port   = conf['MQTT']['PORT']



logger = logging.getLogger('mqtt')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('mqtt.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info('MQTT_SUB...')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("z2", 1883, 60)
client.connect(mqtt_server, mqtt_port, 60)
client.subscribe("tot/yymmdd")
