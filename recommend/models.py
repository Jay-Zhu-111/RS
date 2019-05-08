from django.db import models
# from django.contrib.auth.models import User


class MyUser(models.Model):
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    L = models.CharField(max_length=1000)
    S = models.CharField(max_length=1000)

    def __str__(self):
        return self.user_name


class MyItem(models.Model):
    item_id = models.IntegerField(default=0)
    item_name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
