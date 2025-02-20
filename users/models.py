from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    birth_date = models.DateField("Date of Birth", null=True, blank=True)

    def __str__(self):
        return self.username
