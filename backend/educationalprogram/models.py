from django.db import models


class Educationalprogram(models.Model):
    epId = models.AutoField(primary_key=True)
    Name = models.CharField(default="Разработка информационных систем для бизнеса", max_length=100)
    Code = models.CharField(default="09.03.04", blank=True)

