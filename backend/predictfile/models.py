from django.db import models
import datetime
from filesnew.models import Filesnew

class Predictfile(models.Model):
    predictfileId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    PredictedFile = models.FileField(upload_to='predicted_files/', blank=True, null=True)
    CreatedAt = models.DateField(default=datetime.date.today, blank=True)
    SourceFiles = models.ManyToManyField(Filesnew, related_name='used_in_predictions')
    MinExamScore = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.Name
