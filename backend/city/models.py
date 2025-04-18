from django.db import models


class City(models.Model):
    CityId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)