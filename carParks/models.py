from django.db import models
from django.utils import timezone

class CP(models.Model):
    
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0) 
    #pub_date = models.DateTimeField('date taken', default = 0)
    
    def __str__(self):
        return self.name
    
class CapacityLevel(models.Model):
    
    def __str__(self):
        return self.carParkObj.name
    
    carParkObj = models.ForeignKey(CP)
    name = models.CharField(max_length=100, default = " ", null=True)
    availableSpaces = models.IntegerField(default=0)
    percentFull = models.FloatField(default=0.0)
    dateTaken = models.DateTimeField(default=timezone.now)