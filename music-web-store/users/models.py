from django.db import models
from django.contrib.auth.models import AbstractUser


class WebsiteUser(AbstractUser):
    """
    Stores information about registered users (extends default Django user model)
    """
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True)
    phone_number = models.IntegerField(null=True)
    address = models.TextField(null=True)
    wallet = models.FloatField(null=True, default=0)
