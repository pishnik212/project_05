from django.db import models
from city.models import City

class University(models.Model):
    UniversityId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    CityId = models.ForeignKey(City,  default="Пермь", on_delete=models.SET_DEFAULT)