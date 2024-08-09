from django.contrib.auth.models import User
from django.db import models

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)