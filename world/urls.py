from django.conf.urls import url

from . import views

app_name = 'world'
urlpatterns = [
    url(r'^$', views.airport, name='airport'),
]