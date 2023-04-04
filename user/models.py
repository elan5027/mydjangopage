# Create your models here.
# user/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
