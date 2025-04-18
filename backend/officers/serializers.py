from rest_framework import serializers
from .models import Officer
from user.serializers import UserSerializer

"""
class OfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Officer
        fields = ('officerId',
                  'FirstName',
                  'SecondName',
                  'LastName',
                  'Email'
                  )
                  
# v 02
# Сериализатор для офицера
class OfficerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Включаем сериализатор пользователя

    class Meta:
        model = Officer
        fields = ['user', 'FirstName',
                  'SecondName',
                  'LastName',
                  'Email']
                  
"""
from rest_framework import serializers
from user.models import User
from .models import Officer


class OfficerSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Officer
        fields = ['officerId', 'FirstName',
                  'SecondName',
                  'LastName',
                  'Email']  # или любые твои поля

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(username=user_data['email'], **user_data)
        officer = Officer.objects.create(user=user, **validated_data)
        return officer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.email = user_data.get('email', user.email)
            if user_data.get('password'):
                user.set_password(user_data['password'])
            user.save()

        return super().update(instance, validated_data)