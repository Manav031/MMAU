from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=20, null=True, blank=True)   
    mobile_no = models.CharField(max_length=12, null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    reward_point = models.IntegerField(default=0, blank=True, null=True)
    blood_donated_counter = models.IntegerField(default=0, null=True, blank=True)
    last_blood_donated = models.DateTimeField(null=True, blank=True)

class BloodRequirement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    location = models.TextField()
    units = models.IntegerField()
    mobile_no = models.CharField(max_length=12)
    date = models.DateTimeField(auto_now_add=True)