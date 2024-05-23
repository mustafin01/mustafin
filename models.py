from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fio = models.CharField(max_length=30)
    email = models.EmailField()
    login = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    password = models.CharField(max_length=22)

    REQUIRED_FIELDS = ['fio', 'email', 'login', 'phone', 'password']
    EMAIL_FIELD = 'login'

    def __str__(self):
        return self.login


class Status(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Application(models.Model):
    name = models.CharField(max_length=55)
    auto_num = models.CharField(max_length=20)
    desc = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.auto_num