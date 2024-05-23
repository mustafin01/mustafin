from rest_framework import serializers
from .models import *

class LoginSerializers(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = ['fio', 'email', 'login', 'phone', 'password']

    def save(self, **kwargs):
        user = User(
            fio=self.validated_data['fio'],
            email=self.validated_data['email'],
            login=self.validated_data['login'],
            phone=self.validated_data['phone'],
            username=self.validated_data['login'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        models = Status
        fields = ['name']


class ApplicationSerializers(serializers.ModelSerializer):
    class Meta:
        models = Application
        fields = ['id', 'name', 'auto_num', 'desc', 'status']


class ApplicationSerializersUser(serializers.ModelSerializer):
    class Meta:
        models = Application
        fields = ['name', 'auto_num', 'desc']


class ApplicationSerializersAdmin(serializers.ModelSerializer):
    class Meta:
        models = Application
        fields = ['id', 'name', 'auto_num', 'desc', 'status']