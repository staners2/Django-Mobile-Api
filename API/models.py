from django.db import models

class Countries(models.Model):
    title = models.TextField(null=True)
    prefix = models.TextField(null=True)

class User(models.Model):
    country = models.ForeignKey(Countries, null=True, on_delete=models.SET_NULL, db_constraint=False)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Types(models.Model):
    ru_title = models.TextField(null=True)
    en_title = models.TextField(null=True)

class Histories(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, db_constraint=False)
    type = models.ForeignKey(Types, null=True, on_delete=models.SET_NULL, db_constraint=False)
    date = models.DateField()
    description = models.TextField(null=True)