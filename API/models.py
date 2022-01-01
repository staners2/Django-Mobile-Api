from django.db import models
from django.http import JsonResponse
from rest_framework import status

from API.constant.JsonKey import JsonKey


class Countries(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(null=True)
    prefix = models.TextField(null=True)

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Countries, null=True, on_delete=models.SET_NULL, db_constraint=False)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Types(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(null=True)
    en_title = models.TextField(null=True)

class Histories(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, db_constraint=False)
    type = models.ForeignKey(Types, null=True, on_delete=models.SET_NULL, db_constraint=False)
    number = models.IntegerField(null=True)
    date = models.DateTimeField()
    description = models.TextField(null=True)

class Error():
    messages = None

    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)

class Fact():
    number = None
    text = None
    type = None

    def __init__(self, number, text, type):
        self.number = number
        self.text = text
        self.type = type