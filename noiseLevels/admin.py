from django.contrib import admin

from noiseLevels.models import Meter, Reading

admin.site.register(Meter)
admin.site.register(Reading)