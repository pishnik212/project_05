from rest_framework import serializers
from .models import Educationform


class EducationformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educationform
        fields = ('efId',
                  'Name')