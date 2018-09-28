import paho.mqtt.client as mqtt
import logging
import json
import pymysql
import time
from configure import configure_get
from pprint import pprint
                                                                                  

with open('tot.json','r') as f:
    conf = json.load(f)


pprint(conf)

print("--")

for x in conf:
    print ("%s: %s" % (x, type(conf[x])))
    for y in conf[x]:
        print ("%s: %s" % (y, type(conf[x][y])))
        if type(conf[x][y]) is dict:
            for z in conf[x][y]:
                print("type of %s:%s" % (z, type(z)))
                if type(z) is dict:    
                    print("%s: %s: %s" % (x, y, conf[x][y]))


print( configure_get("MQTT","SERVER") )
print( configure_get("MQTT","PORT") )

