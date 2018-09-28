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

def sync(request, yymmdd, db):
    template = loader.get_template('tot/sync.html')

    if db == 'laravel':
        target_db = 'laravel'
    elif db == 'pg':
        target_db = 'pg'

    ts1  = Tot.objects.using('default').filter(yymmdd=yymmdd).values('yymmdd','accnt').annotate(money=Sum('money'))
    ts2  = Tot.objects.using(target_db).filter(yymmdd=yymmdd).values('yymmdd','accnt').annotate(money=Sum('money'))
    if(len(ts1)==0):
        for ts in ts2:
            print(ts)
            tot = Tot(yymmdd=ts['yymmdd'], accnt=ts['accnt'], money=ts['money'])
            tot.save(using='default')
    elif(len(ts2)==0):
        for ts in ts1:
            print(ts)
            tot = Tot(yymmdd=ts['yymmdd'], accnt=ts['accnt'], money=ts['money'])
            tot.save(using=target_db)
    return list(request)
        

def list(request):
    template = loader.get_template('tot/sync.html')
    ts1  = Tot.objects.using('default').values('yymmdd').annotate(money=Sum('money'))
    ts2  = Tot.objects.using('laravel').values('yymmdd').annotate(money=Sum('money'))
    ts3  = Tot.objects.using('pg').values('yymmdd').annotate(money=Sum('money'))
    ts   = []   
    
    for t1 in ts1:
        t2 = next((item for item in ts2 if item["yymmdd"] == t1["yymmdd"]), False)
        t3 = next((item for item in ts3 if item["yymmdd"] == t1["yymmdd"]), False)
        t  = {}
        t['yymmdd'] = t1['yymmdd']
        t['money1'] = t1['money']

        if t2 != False:
            t['money2'] = t2['money']
        else:
            t['money2'] = False

        if t3 != False:
            t['money3'] = t3['money']
        else:
            t['money3'] = False

        if t['money1'] == t['money2']:
            t['statusL'] = "OK"
        elif t['money2'] == False:
            t['statusL'] = "Sync"
        else:
            t['statusL'] = t['money1'] - t['money2']

        if t['money1'] == t['money3']:
            t['statusP'] = "OK"
        elif t['money3'] == False:
            t['statusP'] = "Sync"
        else:
            t['statusP'] = t['money1'] - t['money3']

        ts.append(t)

    context = {
        'ts1': ts1,
        'ts2': ts2,
        'ts' : ts
        }
    return HttpResponse(template.render(context,request))
