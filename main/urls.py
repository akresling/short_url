from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^newurl/$', views.new_url, name='newurl'),
    url(r'^(?P<visit_url>[0-9A-Za-z]+)/$', views.visit, name='visit'),
]
