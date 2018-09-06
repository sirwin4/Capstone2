from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Area(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    user_area = models.ManyToManyField(User, unique=False)
    lat = models.CharField(max_length=40)
    long = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'area'

    def __str__(self):
        return self.name


class Piece(models.Model):
    name = models.CharField(max_length=30)
    standard_number = models.IntegerField(default=0)
    min_size = models.IntegerField(default=0)
    max_size = models.IntegerField(default=0)
    active = models.BooleanField
    passive = models.BooleanField
    user_rack = models.ManyToManyField(User, unique=False)
    area_rack = models.ManyToManyField(Area, unique=False)

    class Meta:
        db_table = 'piece'

    def __str__(self):
        return self.name



