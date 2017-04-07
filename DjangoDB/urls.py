
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^carParks/', include('carParks.urls')),    
    url(r'^dubBikes/', include('dublinBikes.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls')),
    url(r'^m50/', include('m50times.urls')),
    url(r'^noise/', include('noiseLevels.urls')),
]