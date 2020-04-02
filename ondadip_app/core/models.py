import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=2000)
    created_at = models.DateTimeField('user creation time')
    first_name = models.CharField(max_length=2000)
    last_name = models.CharField(max_length=2000)
    email = models.CharField(max_length=2000)
    is_active = models.BooleanField()

    def __str__(self):
        return self.username

    def add_to_portfolio(self, security):
        up = UserPortfolio(user=self, security=security, created_at=timezone.now(), is_active=True)
        up.save()
        return up.pk


class Security(models.Model):
    symbol = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField('security creation time')

    def __str__(self):
        return self.symbol


class UserPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolio_security")
    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name="portfolio_user")
    created_at = models.DateTimeField('security addition to portfolio time')
    is_active = models.BooleanField()

    def __str__(self):
        return str(self.user) + ": " + str(self.security) + " added at " + str(self.created_at)

    def was_recently_added(self):
        return self.created_at >= (timezone.now() - datetime.timedelta(days=7)).timestamp
