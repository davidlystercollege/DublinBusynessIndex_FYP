from django.db import models
from django.utils import timezone

class Meter(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Reading(models.Model):
    
    def __str__(self):
        return self.rdObj.name
    
    rdObj = models.ForeignKey(Meter)
    name = models.CharField(max_length=100, default = " ", null=True)
    aleq = models.FloatField(default=0.0)
    timeRecorded = models.CharField(max_length=100, default = "99:99:99")
    dateRecorded = models.CharField(max_length=100, default = "00/00/00")
    dateTaken = models.DateTimeField(default=timezone.now)