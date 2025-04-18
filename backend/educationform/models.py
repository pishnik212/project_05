from django.db import models


class Educationform(models.Model):
    efId = models.AutoField(primary_key=True)
    Name = models.CharField(default="Очная", max_length=100)
    # Факультет социально-экономических и компьютерных наук

