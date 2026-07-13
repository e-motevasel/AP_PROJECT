from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLES = [('host', 'Host'), ('guest', 'Guest')]

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
