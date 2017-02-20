from django.db import models
from django.utils import timezone

class DatasetObject(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class BusynessSub(models.Model):
    
    dataObj = models.ForeignKey(DatasetObject)
    name = models.CharField(max_length=100, null=True)
    busynessFactor = models.FloatField(default = 0.0)
    dateTaken = models.DateTimeField(default=timezone.now)
    
    #average = models.FloatField(default = 0.0)
    
    def __str__(self):
        return self.name  
    
class BusynessIndex(models.Model):
    
    busyness = models.FloatField(default = 0.0)
    dateTaken = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(str(self.busyness) + '  :  ' + str(self.dateTaken))