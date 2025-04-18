from rest_framework import serializers
from .models import Educationalprogram


class EducationalprogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educationalprogram
        fields = ('epId',
                  'Name',
                  'Code')