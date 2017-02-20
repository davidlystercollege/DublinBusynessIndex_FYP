from django.db import models
from django.utils import timezone

class Route(models.Model):
    
    name = models.CharField(max_length=100)
    rfrom = models.CharField(max_length=100)
    rto = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Recording(models.Model):
    
    def __str__(self):
        return self.ruObj.name
    
    ruObj = models.ForeignKey(Route)
    name = models.CharField(max_length=100, default = " ", null=True)
    traveltime = models.IntegerField(default=0)
    dateTaken = models.DateTimeField(default=timezone.now)