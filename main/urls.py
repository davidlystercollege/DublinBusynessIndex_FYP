from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='main home'),
    url(r'^test', views.testing, name='Testing Page'),
    url(r'^dash', views.fulldash, name='Full Dashboard'),
    url(r'^dashtest', views.testDash, name='Test Dashboard'),
    url(r'busyness', views.mainBusyness, name='main busyness output'),
]