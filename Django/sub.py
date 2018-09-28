import paho.mqtt.client as mqtt
import json
import sqlite3
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
        try:
                data = json.loads(msg.payload)
                db = sqlite3.connect("/home/pi/Code/Django/db.sqlite3")
                curs = db.cursor()
                sql1="select (1) from tot_tot where yymmdd like ? and accnt like ?"
                sql2="delete from tot_tot where yymmdd like ? and accnt like ?"
                sql3 = "insert into tot_tot(accnt,money,yymmdd) values(?,?,?)"
                for x in range(0, len(data)):
                        print(json.dumps(data[x], indent=4))
                        isexist = curs.execute(sql1, (data[x]["yymmdd"],
                                data[x]["accnt"]))
                        if isexist:
                                curs.execute(sql2,(data[x]["yymmdd"],
                                data[x]["accnt"]))
                        curs.execute(sql3,(data[x]["accnt"],
                                data[x]["money"],
                                data[x]["yymmdd"]))
                db.commit()
                db.close()
        except Exception as e:
                print(str(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("z2", 1883, 60)
client.subscribe("tot/all")

client.loop_start()  #Start loop 
time.sleep(55) 
client.loop_stop()    #Stop loop 
