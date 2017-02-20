from django.contrib import admin

from main.models import DatasetObject, BusynessSub, BusynessIndex

admin.site.register(DatasetObject)
admin.site.register(BusynessSub)
admin.site.register(BusynessIndex)
