from django.urls import path

from . import views
from . import mqtt
from . import sync
from . import sync
from . import remote
from . import serialize

urlpatterns = [
    path('', 							views.daily, 	name='index'),
    path('get_name', 					views.get_name, name='index'),
    path('daily',  						views.daily,  	name='daily'),
    path('today',  						views.today,  	name='today'),
    path('detail',  					views.detail,  	name='detail'),
    path('accnt/<slug:accnt>',      	views.accnt,  	name='accnt'),
    path('<int:yymmdd>/', 				views.yymmdd, 	name='yymmdd'),
    path('totf',  						views.totf, 	name='totf'),
    path('totf/<int:yymmdd>',	    	views.totfyymmdd,name='totfyymmdd'),
    path('pub',  						mqtt.pub,  	name='pub'),
    path('pub/<int:yymmdd>',	    	mqtt.pubyymmdd,	name='pubyymmdd'),
    path('sync',	                	sync.list,	name='list'),
    path('sync/<int:yymmdd>/<slug:db>', sync.sync,	name='sync'),
    path('serialize',                   serialize.serialize,	name='serialize'),
    path('getjson',                   	serialize.getjson,	name='getjson'),
    path('getjsonf',                   	remote.getjsonf,	name='getjsonf'),
    path('thanks',  					views.thanks,  	name='thanks'),
]
