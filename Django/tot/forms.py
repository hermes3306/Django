from django import forms

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name',max_length=100)

class TotForm(forms.Form):
	yymmdd 		= forms.IntegerField(label='yymmdd:')
	kw 			= forms.IntegerField(label='kw:')
	wr1 		= forms.IntegerField(label='wr1:')
	wr2 		= forms.IntegerField(label='wr2:')
	ha 			= forms.IntegerField(label='ha:')
	wo 			= forms.IntegerField(label='wo:')
	xi 			= forms.IntegerField(label='xi:')
	hd 			= forms.IntegerField(label='hd:')
	ok 			= forms.IntegerField(label='ok:')

class getjsonForm(forms.Form): 
	url 		= forms.URLField(initial='http://z1:9000/tot/getjson')
	target 		= forms.CharField(initial='default')
