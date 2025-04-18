from rest_framework import serializers
from .models import Predictfile
from filesnew.models import Filesnew
from filesnew.serializers import FilesnewSerializer
import math


class PredictfileSerializer(serializers.ModelSerializer):
    SourceFiles = FilesnewSerializer(many=True, read_only=True)

    class Meta:
        model = Predictfile
        fields = ['predictfileId', 'Name', 'PredictedFile', 'CreatedAt', 'MinExamScore', 'SourceFiles']


