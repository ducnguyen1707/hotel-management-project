from django.conf import settings
from django.db import models


# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_rooms= models.IntegerField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField(max_length=11)
    
class RoomCategory(models.Model):
    roomtype = models.CharField(max_length=50)
    description = models.CharField( max_length=50)
    floor = models.IntegerField()
    
    def __str__(self) :
        return self.roomtype
    
class Client(models.Model):
    pass

class ClientList(models.Model):
    pass

class RoomManage(models.Model):
    roomnumber = models.IntegerField()

class Bill(models.Model):
    pass

class StaffSchedule(models.Model):
    shift_name= models.CharField( max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    
class Staff(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="staff_name")
    schedule = models.ForeignKey(StaffSchedule, on_delete= models.CASCADE)
    



class Reporting(models.Model):
    pass