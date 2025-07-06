from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # In future: add 2FA, profile image, etc.
    def __str__(self):
        return self.username