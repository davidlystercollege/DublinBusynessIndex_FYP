from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='main home'),
    url(r'^main', views.mainHome, name='main home extra page'),
    url(r'busyness', views.mainBusyness, name='main busyness output'),
]