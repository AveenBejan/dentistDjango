
from django.db import models
from django.contrib.auth.models import User


class Reception(models.Model):
    name = models.CharField('Name',max_length=120)
    phone = models.CharField('Name',max_length=120)

    def __str__(self):
        return self.name


class OralSurgery(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE,blank=True)
    tooth = models.CharField('tooth',max_length=120)
    RX = models.CharField('RX',max_length=120,blank=True)
    material_type = models.CharField('material_type',max_length=120,blank=True)
    thickness_rich = models.CharField('thickness_rich', max_length=120,blank=True)
    size = models.CharField('size',max_length=120,blank=True)
    size_direction = models.CharField('size_direction', max_length=120, blank=True)
    size_number = models.CharField('size_number', max_length=120, blank=True)
    second_visit = models.CharField('second_visit', max_length=120,blank=True)
    third_visit = models.CharField('third_visit', max_length=120,blank=True)
    fourth_visit = models.CharField('fourth_visit', max_length=120,blank=True)
    fifth_visit = models.CharField('fifth_visit', max_length=120,blank=True)

    def __str__(self):
        return self.idReception


class Contact(models.Model):
    name = models.CharField('Name',max_length=120)
    email = models.EmailField('Email Address')
    subject = models.CharField('Address',max_length=300)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Appointment1(models.Model):
    name = models.CharField('Name',max_length=120)
    gender = models.CharField('Gender', max_length=50)
    birthday = models.DateTimeField()
    email = models.EmailField('Email Address')
    address = models.CharField('Address',max_length=300)
    date = models.DateTimeField()
    phone = models.CharField('Phone',max_length=20)

    def __str__(self):
        return self.name


class DentistDetails(models.Model):
    idappointment = models.ForeignKey(Appointment1,on_delete=models.CASCADE)
    details = models.TextField('Details', max_length=200)
    medicine_name = models.CharField('Medicine Name',max_length=300)
    medicine_time = models.CharField('Medicine Time',max_length=50)
    medicine_period = models.CharField('Medicine Period',max_length=50)
    medicine_tfood = models.CharField('Medicine T-Food',max_length=50)
    medicine_no = models.CharField('Medicine No',max_length=20)

    def __str__(self):
        return self.details


class Orthodontics(models.Model):
    name = models.CharField(max_length=100,)
    yes_no_field = models.CharField(max_length=100)
    material_field = models.CharField(max_length=100)
    width_field = models.CharField(max_length=100)