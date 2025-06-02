from rest_framework import serializers
from .models import Emptyfile
from university.models import University

from rest_framework import serializers
from .models import Emptyfile
from university.models import University
from datetime import timedelta


class EmptyfileSerializer(serializers.ModelSerializer):
    UniversityName = serializers.CharField(source='UniversityId.Name', read_only=True)
    CityName = serializers.CharField(source='UniversityId.CityId.Name', read_only=True)
    EPName = serializers.CharField(source='EPId.Name', read_only=True)
    EFName = serializers.CharField(source='EFId.Name', read_only=True)
    FacultyName = serializers.CharField(source='FacultyId.Name', read_only=True)

    DownloadOfficer = serializers.SerializerMethodField()

    def get_DownloadOfficer(self, obj):
        officer = obj.DownloadOfficerId
        if officer:
            return f"{officer.LastName} {officer.FirstName[0]}. {officer.SecondName[0]}."
        return ""

    class Meta:
        model = Emptyfile
        fields = ['fileId', 'Name', 'DownloadDate', 'DownloadOfficer', 'AdmissionYear',
                  'UniversityName', 'CityName', 'Emptyfile', 'EFName' , 'EPName' , 'FacultyName', 'Description'
                  ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.DownloadDate:
            # Прибавляем 5 часов
            shifted_datetime = instance.DownloadDate + timedelta(hours=5)
            data['DownloadDate'] = shifted_datetime.strftime('%d.%m.%Y %H:%M')  # можно настроить формат
        return data

from rest_framework import serializers
from .models import Emptyfile


from rest_framework import serializers
from .models import Emptyfile
from university.models import University

class EmptyfileCreateSerializer(serializers.ModelSerializer):
    # UniversityId = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = Emptyfile
        fields = ['Name', 'DownloadDate', 'DownloadOfficerId', 'AdmissionYear', 'UniversityId', 'Emptyfile'
                                    , 'EPId' , 'EFId', 'FacultyId', 'Description'
            # , 'EPName' , 'EFName', 'FacultyName', 'Description'
        ]
