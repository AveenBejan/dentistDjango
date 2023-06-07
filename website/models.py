
from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField('Name',max_length=120)
    email = models.EmailField('Email Address')
    subject = models.CharField('Address',max_length=300)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    name = models.CharField('Name',max_length=120)
    email = models.EmailField('Email Address',blank=True)
    address = models.CharField('Address',max_length=300,blank=True)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    phone = models.CharField('Phone',max_length=20,blank=True)

    def __str__(self):
        return self. name