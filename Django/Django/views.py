# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect

def daily(request):
	return HttpResponseRedirect('/tot/daily')
