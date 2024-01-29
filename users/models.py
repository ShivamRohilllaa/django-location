from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=100)
    location = models.PointField(blank=True, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.name
    
    