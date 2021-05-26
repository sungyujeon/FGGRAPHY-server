from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    point = models.IntegerField(default=0)
    ranking = models.IntegerField(null=True, default=10000000)
    tier = models.IntegerField(null=True, default=5)



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
