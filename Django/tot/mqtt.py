# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.db.models import Sum
from .models import Tot
import datetime
import pymysql
import sqlite3
import json
import paho.mqtt.client as mqtt
import time

def pubyymmdd(request, yymmdd):
	ts = Tot.objects.filter(yymmdd=yymmdd).values('id','yymmdd','accnt','money').annotate()
	if(len(ts) == 0):
		return HttpResponseRedirect('/tot/totf')
	msg = []
	for t in ts:
		j = {'id': t['id'], 'accnt': t['accnt'], 'money': t['money'], 'yymmdd': t['yymmdd']}
		msg.append(j)
	jmsg = json.dumps(msg,indent=4)

	client = mqtt.Client()
	client.connect("localhost",1883, 60)
	client.publish("tot/yymmdd", jmsg)
	template = loader.get_template('tot/pub.html')
	context = {
		'ts': ts,
		'jmsg': jmsg,
	}
	return HttpResponse(template.render(context,request))

def pub(request):
	d = datetime.date.today()
	to_day = d.strftime("%y%m%d")
	return pubyymmdd(request, to_day)
