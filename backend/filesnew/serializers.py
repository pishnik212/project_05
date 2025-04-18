from rest_framework import serializers
from .models import Filesnew
from university.models import University

# Норм
"""
class FilesnewSerializer(serializers.ModelSerializer):
    UniversityName = serializers.CharField(source='UniversityId.Name', read_only=True)
    CityName = serializers.CharField(source='UniversityId.CityId.Name', read_only=True)  # Добавляем город

    class Meta:
        model = Filesnew
        fields = ['fileId', 'Name', 'DownloadDate', 'DownloadOfficerId', 'AdmissionYear',
                  'UniversityName', 'CityName',
                  'Filesnew']
"""


from rest_framework import serializers
from .models import Filesnew
from university.models import University
from educationalprogram.models import Educationalprogram
from datetime import timedelta

class FilesnewSerializer(serializers.ModelSerializer):
    UniversityName = serializers.CharField(source='UniversityId.Name', read_only=True)
    CityName = serializers.CharField(source='UniversityId.CityId.Name', read_only=True)
    EPName = serializers.CharField(source='EPId.Name', read_only=True)
    EFName = serializers.CharField(source='EFId.Name', read_only=True)
    FacultyName = serializers.CharField(source='FacultyId.Name', read_only=True)
    DownloadDate = serializers.DateTimeField(format="%d.%m.%Y %H:%M")


    # 👇 Формируем фамилию и инициалы из Officer
    DownloadOfficer = serializers.SerializerMethodField()

    def get_DownloadOfficer(self, obj):
        officer = obj.DownloadOfficerId
        # print("DEBUG OFFICER:", officer)  # ← добавь это
        if officer:
            return f"{officer.LastName} {officer.FirstName[0]}. {officer.SecondName[0]}."
        return ""

    class Meta:
        model = Filesnew
        fields = [
            'fileId', 'Name', 'DownloadDate', 'DownloadOfficer', 'AdmissionYear',
            'UniversityName', 'CityName', 'Filesnew', 'EPName' , 'EFName', 'FacultyName', 'Description'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.DownloadDate:
            # Прибавляем 5 часов
            shifted_datetime = instance.DownloadDate + timedelta(hours=5)
            data['DownloadDate'] = shifted_datetime.strftime('%d.%m.%Y %H:%M')  # можно настроить формат
        return data


from rest_framework import serializers
from .models import Filesnew


from rest_framework import serializers
from .models import Filesnew
from university.models import University

class FilesnewCreateSerializer(serializers.ModelSerializer):
    # UniversityId = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = Filesnew
        fields = ['Name', 'DownloadDate',  'AdmissionYear', 'UniversityId', 'Filesnew'
            , 'EPId' , 'EFId', 'FacultyId', 'Description'
            # , 'EPName', 'EFName', 'FacultyName', 'Description'
                  ]



    """
    class Meta:
        model = Filesnew

        fields = '__all__'
        read_only_fields = ('fileId',)
    """
