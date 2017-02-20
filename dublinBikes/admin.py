from django.contrib import admin

from dublinBikes.models import BikeStation, Availability

admin.site.register(BikeStation)
admin.site.register(Availability)