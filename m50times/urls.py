from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='m50 home'),
    url(r'times', views.m50times, name='m50times page'),
    url(r'times', views.m50dataset, name='m50times data'),
]