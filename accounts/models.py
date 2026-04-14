from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('coordinator','Coordinator'),
        ('guide','Guide'),
        ('student','Student'),
    )
    user_role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='student')

    def __str__(self):
        return self.username
