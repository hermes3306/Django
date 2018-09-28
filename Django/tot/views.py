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

def daily(request):
	template = loader.get_template('tot/daily.html')
	ts	=	Tot.objects.values('yymmdd')
	res = ts.annotate(daily_total=Sum('money'))
	ts  = Tot.objects.values('yymmdd').annotate(money=Sum('money'))
	legend_array 	= []
	amounts_array = []
	gap = 0
	inx = 0 
	gap_array = []
	sum = 0
	money_0 = 0
	
	for t in ts:
		if inx in [0]:
			before = t['money'] 
			money_0  = t['money'] 
		legend_array.append(t['yymmdd']) 
		amounts_array.append(t['money']) 
		gap_array.append(t['money'] - before)
		t['gap'] = t['money'] - before
		if t['gap'] > 0:
			t['color'] = '#FF0000'
		else:
			t['color'] = '#0000FF'
		sum = sum + t['gap']
		if t['money'] > money_0:
			t['color2'] = '#FF0000'
		else:
			t['color2'] = '#0000FF'
		t['sum'] = sum
		before = t['money'] 
		inx = inx+1
		
	legend  = ' ,'.join(str(e) for e in legend_array)
	amounts = ' ,'.join(str(e) for e in amounts_array)
	gaps 	= ' ,'.join(str(e) for e in gap_array)

	context = {
		'ts': ts,
		'legend': legend,
		'title': 'Daily Sum:',
		'moneys': amounts,
		'rgb': '#0000FF',
		'gaps': gaps,
	}
	return HttpResponse(template.render(context,request))

def rgbmap(x):
	return {'kw':'rgb(0,255,0)', 'wr1': 'rgb(0,0,255)',\
		 'wr2': 'rgb(255,0,0)', 'ok':'rgb(0,255,0)',\
		 'hd': 'rgb(0,0,255)', 'xi': 'rgb(255,0,0)',\
		 'ha':'rgb(128,0,0)', 'wo': 'rgb(128,128,128)' }[x] 

def today(request):
	d = datetime.date.today()
	to_day = d.strftime("%y%m%d")
	return yymmdd(request, to_day)

def detail(request):
	template = loader.get_template('tot/detail.html') 
	accnts=['kw','wr1','wr2','hd','ha', 'wo','xi','ok']
	legend_array = []
	amounts_array = []
	inx = 0
	for accnt in accnts:
		ts = Tot.objects.filter(accnt=accnt).order_by('yymmdd').values('yymmdd').annotate(amount=Sum('money'))
		arr = []
		for t in ts:
			if inx in [0]: 
				legend_array.append(t['yymmdd'])
			arr.append(t['amount'])
		amounts_array.append(arr)
		inx = inx + 1

	legend  = ' ,'.join(str(e) for e in legend_array)
	amount  = []
	for amounts in amounts_array:
		amount.append(' ,'.join(str(e) for e in amounts))
	print(amount[1])

	rgb =  rgbmap(accnt)
	accnts=['kw','wr1','wr2','hd','ha', 'wo','xi','ok']

	moneys = {'kw': amount[0], 	'wr1': amount[1], 'wr2': amount[2], \
				'hd': amount[3], 'ha': amount[4], 'wo': amount[5], \
				'xi': amount[6], 'ok': amount[7] } 
	rgbs = {'kw': rgbmap(accnts[0]), 'wr1': rgbmap(accnts[1]), \
				'wr2': rgbmap(accnts[2]), 'hd': rgbmap(accnts[3]), \
				'ha': rgbmap(accnts[4]),  'wo': rgbmap(accnts[5]), \
				'xi': rgbmap(accnts[6]),  'ok': rgbmap(accnts[7]) }
	ts = Tot.objects.order_by('yymmdd').all()

	context = {
		'ts': ts,
		'accnt': accnts,
		'legend': legend,
		'rgbs': rgbs,
		'amount': amount,
		'moneys': moneys,
		'kw': amount[0],
		'wr1': amount[1],
		'wr2': amount[2],
		'hd': amount[3],
		'ha': amount[4],
		'wo': amount[5],
		'xi': amount[6],
		'ok': amount[7],
	}
	return HttpResponse(template.render(context,request))

def yymmdd(request,yymmdd):
	try:
		ts = Tot.objects.filter(yymmdd=yymmdd).values('yymmdd','accnt','money').annotate()
		if(len(ts) == 0):
			return HttpResponseRedirect('/tot/totf')
		print(len(ts))
		legend_array = []
		money_array = []
		rgb_array = []
		
		for t in ts:
			legend_array.append(t['accnt'])
			money_array.append(t['money'])
			rgb = rgbmap(t['accnt'])
			rgb_array.append(rgb)

		amount = ' ,'.join(str(e) for e in money_array)

		template = loader.get_template('tot/yymmdd.html')
		context = {
			'ts': ts,
			'legend': legend_array,
			'amount': amount,
			'rgbs': rgb_array,
		}
	except Tot.DoesNotExist:
		raise Http404("Tot does not exist")
	return HttpResponse(template.render(context,request))

def accnt(request,accnt):
	try:
		ts = Tot.objects.filter(accnt=accnt).order_by('yymmdd').values('yymmdd','money')
		legend_array = []
		money_array = []
		rgb_array = []
		gap = 0
		inx = 0 
		gap_array = []
		sum = 0
		money_0 = 0
		
		for t in ts:
			if inx in [0]:
				before = t['money']
				money_0  = t['money']
			legend_array.append(t['yymmdd'])
			money_array.append(t['money'])
			t['gap'] = t['money'] - before
			if t['gap'] > 0:
				t['color'] = '#FF0000'
			else:
				t['color'] = '#0000FF'
			sum = sum + t['gap']
			if t['money'] > money_0:
				t['color2'] = '#FF0000'
			else:
				t['color2'] = '#0000FF'

			t['sum'] = sum 
			before = t['money']
			inx=inx+1

		legend = ' ,'.join(str(e) for e in legend_array)
		amounts = ' ,'.join(str(e) for e in money_array)
		template = loader.get_template('tot/accnt.html')
		rgb = rgbmap(accnt)
		context = {
			'ts': ts,
			'title': accnt,
			'legend': legend,
			'moneys': amounts, 
			'rgb': rgb,
		}
		print(ts)
		print(legend)
		print(amounts)
		print(rgb)
	except Tot.DoesNotExist:
		raise Http404("Tot does not exist")
	return HttpResponse(template.render(context,request))

def thanks(request):
	context = {
		'msg': 'thanks',
	}
	template = loader.get_template('tot/thanks.html')
	return HttpResponse(template.render(context,request))
	

def get_name(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/tot/thanks')
	else:
		form = NameForm()
	return render(request, 'tot/name.html', {'form': form})

def totf(request):
	ts = Tot.objects.all().aggregate(Max('yymmdd'))
	yymmdd = ts['yymmdd__max']
	return totfyymmdd(request,yymmdd)

def totfyymmdd(request,yymmdd):
	if request.method == 'POST':
		form = TotForm(request.POST)

		if form.is_valid():
			yymmdd 	= form.cleaned_data['yymmdd']
			Tot.objects.filter(yymmdd=yymmdd).delete()

			kw 		= form.cleaned_data['kw']
			wr1		= form.cleaned_data['wr1']
			wr2		= form.cleaned_data['wr2']
			ha		= form.cleaned_data['ha']
			wo		= form.cleaned_data['wo']
			xi		= form.cleaned_data['xi']
			hd		= form.cleaned_data['hd']
			ok		= form.cleaned_data['ok']

			tot = Tot(yymmdd=yymmdd, accnt='kw', money=kw)
			tot.save()
			tot = Tot(yymmdd=yymmdd, accnt='wr1', money=wr1)
			tot.save()
			tot = Tot(yymmdd=yymmdd, accnt='wr2', money=wr2)
			tot.save()
			tot = Tot(yymmdd=yymmdd, accnt='ha', money=ha)
			tot.save()
			tot = Tot(yymmdd=yymmdd, accnt='wo', money=wo)
			tot.save()
			tot = Tot(yymmdd=yymmdd, accnt='xi', money=xi)
			tot.save()
			tot = Tot(yymmdd=yymmdd, accnt='hd', money=hd)
			tot.save()
			tot = Tot(yymmdd=yymmdd, accnt='ok', money=ok)
			tot.save()

			return HttpResponseRedirect('/tot/%s'%yymmdd)
	else:
		val = Tot.objects.filter(yymmdd=yymmdd,accnt='kw').values('money').annotate()[0]
		kw = val['money']

		val = Tot.objects.filter(yymmdd=yymmdd,accnt='wr1').values('money').annotate()[0]
		wr1 = val['money']

		val = Tot.objects.filter(yymmdd=yymmdd,accnt='wr2').values('money').annotate()[0]
		wr2 = val['money']

		val = Tot.objects.filter(yymmdd=yymmdd,accnt='ha').values('money').annotate()[0]
		ha = val['money']

		val = Tot.objects.filter(yymmdd=yymmdd,accnt='wo').values('money').annotate()[0]
		wo = val['money']

		val = Tot.objects.filter(yymmdd=yymmdd,accnt='xi').values('money').annotate()[0]
		xi = val['money']

		val = Tot.objects.filter(yymmdd=yymmdd,accnt='hd').values('money').annotate()[0]
		hd = val['money']

		val = Tot.objects.filter(yymmdd=yymmdd,accnt='ok').values('money').annotate()[0]
		ok = val['money']

		lastval = {'yymmdd': yymmdd,
					'kw': kw,
					'wr1': wr1,
					'wr2': wr2,
					'ha': ha,
					'wo': wo,
					'xi': xi,
					'hd': hd,
					'ok': ok,
					}
		form = TotForm(initial=lastval)
	return render(request, 'tot/totf.html', {'form': form})
	
