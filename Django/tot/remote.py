# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum, Max
from .models import Tot
from .models import SM
import datetime
from .forms import NameForm
from .forms import TotForm
from .forms import getjsonForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import serializers
import urllib
from urllib.request import urlopen
import json

def getjsonf(request):
	if request.method == 'POST':
		form = getjsonForm(request.POST)
		if form.is_valid():
			url 		= form.cleaned_data['url']
			target 		= form.cleaned_data['target']
			with urlopen(url) as request:
				databin = request.read()
			jmsg = databin.decode('utf-8');
			data = json.loads(jmsg)
			jarr = json.loads(data['Tot'])
			Tot.objects.using(target).all().delete()
			for j in jarr:
				tot = Tot(yymmdd=j['yymmdd'], accnt=j['accnt'], money=j['money'])
				tot.save(using=target)
		else:
			return HttpResponseRedirect('/tot/getjsonf')
		return HttpResponseRedirect('/tot/sync')

	else:
		remoteurl = 1
		initval = { 'url':	 	'http://118.221.137.114:9000/tot/getjson',
					'target':	'default'
					}
		form = getjsonForm(initial=initval)
	return render(request, 'tot/getjsonf.html', {'form': form})
	
