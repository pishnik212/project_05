from django.db import models
import datetime
import os
from officers.models import Officer
from university.models import University
from city.models import City
from educationalprogram.models import Educationalprogram
from faculty.models import Faculty
from educationform.models import Educationform
from django.utils import timezone

def upload_to(instance, filename):
    return os.path.join('empty', str(datetime.date.today().year), filename)


class Emptyfile(models.Model):
    fileId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    # DownloadDate = models.DateField(default=datetime.date.today, blank=True)
    DownloadDate = models.DateTimeField(default=timezone.now, blank=True)
    DownloadOfficerId = models.ForeignKey(Officer, default=1, on_delete=models.SET_DEFAULT, blank=True)
    AdmissionYear = models.IntegerField(default=2025, blank=True)
    Emptyfile = models.FileField(upload_to=upload_to, blank=True, null=True)  # Новое поле для файла
    UniversityId = models.ForeignKey(University, on_delete=models.SET_DEFAULT, default=1, blank=True)
    EPId = models.ForeignKey(Educationalprogram, on_delete=models.SET_DEFAULT, default=1, blank=True)
    EFId = models.ForeignKey(Educationform, on_delete=models.SET_DEFAULT, default=1, blank=True)
    FacultyId = models.ForeignKey(Faculty, on_delete=models.SET_DEFAULT, default=1, blank=True)
    Description = models.CharField(max_length=1000, default='', blank=True)

