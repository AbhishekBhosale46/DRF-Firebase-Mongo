from django.db import models

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
