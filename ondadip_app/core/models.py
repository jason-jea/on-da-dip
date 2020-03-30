from django.db import models


class User(models.Model):
    username = models.CharField(max_length=2000)
    created_at = models.DateTimeField('user creation time')
    first_name = models.CharField(max_length=2000)
    last_name = models.CharField(max_length=2000)
    email = models.CharField(max_length=2000)
    is_active = models.BooleanField()


class Security(models.Model):
    symbol = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField('security creation time')


class UserPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    created_at = models.DateTimeField('security addition to portfolio time')
    is_active = models.BooleanField()


