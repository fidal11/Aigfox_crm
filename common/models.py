from django.db import models
import datetime
from django.utils import timezone
# Create your models here.



class ClockInClockOut(models.Model):
    timestamp = models.DateTimeField()
    clock_type = models.CharField(max_length=10)  
    email = models.EmailField()   
    
    class Meta:
        db_table = 'clockinclockout_tb'
     
    
    
class Break(models.Model):
    timestamp_start = models.DateTimeField(null=True)
    timestamp_end = models.DateTimeField(null=True)
    email = models.EmailField()   
    class Meta:
        db_table = 'break_tb'


