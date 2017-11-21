from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^$', views.post, name='main'),
    url(r'^callback/$', views.callback, name='auth_return'),
    url(r'^logout/$', views.unauth, name='oauth_unauth'),
    url(r'^auth/$', views.auth, name='oauth_auth'),
    url(r'^info/$', views.post, name='info'),
    url(r'^profile$', views.post_list, name='profile'),
    url(r'^post_info/(?P<pk>\d+)/$', views.post_info, name='post_info')
]
