from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField, DateField, PositiveIntegerField

CHOICES = (("0", "PENDING"), ("1", "BOUGHT"), ("2", "NOT AVAILABLE"))


class Grocery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = CharField(max_length=50, null=False, blank=False)
    quantity = PositiveIntegerField(null=False, blank=False)
    status = CharField(max_length=1, choices=CHOICES)
    date = DateField(null=False, blank=False)


class ProfileModel(User):
    pass
