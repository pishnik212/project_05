from django.db import models


class Faculty(models.Model):
    facultyId = models.AutoField(primary_key=True)
    Name = models.CharField(default="Факультет социально-экономических и компьютерных наук", max_length=100)
    # Факультет социально-экономических и компьютерных наук

