from django.db import models
from django.contrib.auth.models import User

from backend import settings


class Officer(models.Model):
    officerId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    SecondName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ссылка на кастомного пользователя
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"
