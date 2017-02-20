from django.db import models
from django.utils import timezone

class BikeStation(models.Model):
    
    name = models.CharField(max_length=100)
    totalBikeStands = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Availability(models.Model):
    
    def __str__(self):
        return self.bsObj.name
    
    bsObj = models.ForeignKey(BikeStation)
    name = models.CharField(max_length=100, default = " ", null=True)
    availableBikes = models.IntegerField(default=0)
    availableStands = models.IntegerField(default=0)
    percentFull = models.FloatField(default=0.0)
    dateTaken = models.DateTimeField(default=timezone.now)