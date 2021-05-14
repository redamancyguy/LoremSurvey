from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20, default=None, unique=True)
    password = models.CharField(max_length=100, default=None)
    # token = models.CharField(max_length=100, default=None)
    token = models.TextField(max_length=1024, default=None)
    phone = models.CharField(max_length=15, default=None)
    email = models.CharField(max_length=20, default=None)