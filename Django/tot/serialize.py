# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum, Max
from .models import Tot
from .models import SM
import datetime
from .forms import NameForm
from .forms import TotForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import serializers
from django.http import JsonResponse
import json
import simplejson

def getjson(request):
	ts = Tot.objects.values('id','yymmdd','accnt','money').annotate()
	msg = [] 
	for t in ts:
		j = {'id': t['id'], 'accnt': t['accnt'], 'money': t['money'], 'yymmdd': t['yymmdd']}
		msg.append(j)
	jmsg = json.dumps(msg)
	jjmsg = {'Tot': jmsg}
	return JsonResponse(jjmsg)

def serialize(request):
    template = loader.get_template('tot/serialize.html')
    str = datetime.datetime.now().strftime("%y%m%d%H%M%S")

    with open("tot-%s.xml"%(str), "w") as out:
        serializers.serialize('xml', Tot.objects.all(), stream=out)

    with open("tot-%s.json"%(str), "w") as out:
        serializers.serialize('json', Tot.objects.all(), stream=out)

    #xml = serializers.serialize('xml', Tot.objects.all(), fields=('yymmdd','accnt', 'money'))
    xml = serializers.serialize('xml', Tot.objects.all())
    jso = serializers.serialize('json', Tot.objects.all())   

    cnt1 = Tot.objects.using("pg").all().count()
    cnt2 = Tot.objects.using("laravel").all().count()

    Tot.objects.using("pg").all().delete()
    Tot.objects.using("laravel").all().delete()

    for ts in serializers.deserialize("xml", xml):
        ts.save(using="pg")

    for ts in serializers.deserialize("json", jso):
        print(ts)
        ts.save(using="laravel")

    context = {
        'cnt1' : cnt1,
        'cnt2' : cnt2,
    }

    return HttpResponse(template.render(context,request))
