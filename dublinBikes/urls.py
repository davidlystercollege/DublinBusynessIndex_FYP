from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'db', views.dubBikes, name='dublinBikes'),
]