from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    point = models.IntegerField(default=0)
    ranking = models.IntegerField(null=True, default=None)
    tier = models.IntegerField(null=True, default=None)


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
