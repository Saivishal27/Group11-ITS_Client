from django.conf.urls import url

from . import views
urlpatterns = [

    url(r'^its/House/$', views.House, name='House'),
    url(r'^its/Farm/$', views.Farm, name='Farm'),
    url(r'^its/index/$', views.index, name='index'),
    url(r'^its/Well/$', views.Well, name='Well')

    
]
