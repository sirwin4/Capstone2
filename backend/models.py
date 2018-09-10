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
    SLCD = models.BooleanField(default=False)
    user_rack = models.ManyToManyField(User, through='Userrack')
    area_rack = models.ManyToManyField(Area, through='Arearack')

    class Meta:
        db_table = 'piece'

    def __str__(self):
        return self.name

class Userrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class Arearack(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
