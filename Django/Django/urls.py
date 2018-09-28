from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('',    views.daily,    name='index'),
	path('admin/', admin.site.urls),
	path('tot/', include('tot.urls')),
	
]
