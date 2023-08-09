
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class Doctors(models.Model):
    doctor_name = models.CharField('doctor_name',max_length=120)
    phone = models.CharField('phone',max_length=120)
    gender = models.CharField('Gender',max_length=20)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)

    def __str__(self):
        return self.doctor_name


class Reception(models.Model):
    name = models.CharField('Name',max_length=120)
    phone = models.CharField('phone',max_length=120)
    gender = models.CharField('Gender',max_length=20)
    date_of_birth = models.DateField()
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True,null=False)
    time = models.CharField(null=True,max_length=200)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)

    def __str__(self):
        return self.name


class Filling(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('date_of_birth', max_length=20,null=False)
    filling_type = models.CharField('filling_type', max_length=120, blank=True,null=False)
    filling_place = models.CharField('filling_place',max_length=120, blank=True,null=False)
    ur = models.CharField('ur', max_length=120, blank=True,null=True)
    ul = models.CharField('ul', max_length=120, blank=True,null=True)
    lr = models.CharField('lr', max_length=120,null=True, blank=True)
    ll = models.CharField('ll', max_length=120,null=True, blank=True)
    no_prepare = models.IntegerField('no_prepare',null=False)
    price = models.DecimalField('price',max_digits=8,decimal_places=2,null=False)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=2, null=False)
    note = models.CharField('note', max_length=120, blank=True,null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')


class Crown(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    shade = models.CharField('shade', max_length=120, blank=True,null=False)
    no_unite = models.CharField('no_unite',max_length=120, blank=True,null=False)
    color = models.CharField('color', max_length=120, blank=True,null=False)
    no_prepare = models.IntegerField('no_prepare',  blank=True,null=False)
    price = models.DecimalField('price',max_digits=8,decimal_places=2,null=False)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=2,null=False)
    note = models.CharField('note', max_length=120, blank=True,null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')


class Veneer(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    shade = models.CharField('shade', max_length=120, blank=True,null=False)
    no_unite = models.CharField('no_unite',max_length=120, blank=True,null=False)
    color = models.CharField('color', max_length=120, blank=True,null=False)
    no_prepare = models.IntegerField('no_prepare', blank=True,null=False)
    price = models.DecimalField('price',max_digits=8,decimal_places=2,null=False)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=2,null=False)
    note = models.CharField('note', max_length=120, blank=True,null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')


class Medicine1(models.Model):
    name_medicine = models.CharField(max_length=120)

    def __str__(self):
        return self.name_medicine


class Drug(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    name_medicine = models.CharField(max_length=200, blank=True,null=False)  # This should be a CharField, not ForeignKey
    name = models.CharField('Name', max_length=120,blank=True,null=False)
    phone = models.CharField('Phone', max_length=120,blank=True,null=False)
    gender = models.CharField('Gender', max_length=20,blank=True,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,blank=True,null=False)
    doze = models.CharField(max_length=200,blank=True,null=False)
    type = models.CharField(max_length=200,blank=True,null=False)
    times = models.CharField(max_length=200,blank=True,null=False)
    regdate = models.DateTimeField('Regdate', auto_now_add=True, editable=False)


class Exo(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    ur = models.CharField('Name',max_length=120, blank=True,null=True)
    ul = models.CharField('Name', max_length=120, blank=True,null=True)
    lr = models.CharField('Name', max_length=120, blank=True,null=True)
    ll = models.CharField('Name', max_length=120, blank=True,null=True)
    no_prepare = models.IntegerField('no_prepare', blank=True,null=False)
    price = models.DecimalField('price',max_digits=20,decimal_places=2,null=False)
    total_price = models.DecimalField('total_price', max_digits=20, decimal_places=2,null=False)
    note = models.CharField('Name', max_length=120, blank=True,null=True)
    exoby = models.CharField('Name', max_length=120, blank=True,null=True)
    simpleexo = models.CharField('Name', max_length=120, blank=True,null=True)
    complcated = models.CharField('Name', max_length=120, blank=True,null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')

    def __str__(self):
        return self.name


class Photo(models.Model):
    exo_instance = models.ForeignKey(Exo, on_delete=models.CASCADE,null=True)
    crown_instance = models.ForeignKey(Crown, on_delete=models.CASCADE,null=True)
    veneer_instance = models.ForeignKey(Veneer, on_delete=models.CASCADE, null=True)
    filling_instance = models.ForeignKey(Filling, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')

    def __str__(self):
        return str(self.id)


class Medicin(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE,blank=True)
    name = models.CharField('Name',max_length=120)
    phone = models.CharField('Phone', max_length=120)
    gender = models.CharField('Gender', max_length=20)
    date_of_birth = models.CharField('Gender', max_length=20)
    antibiotic = models.CharField('antibiotic',max_length=120, blank=True)
    analogous = models.CharField('analogous', max_length=120, blank=True)
    mouthwash = models.CharField('mouthwash', max_length=120, blank=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True, editable=False)

    def __str__(self):
        return self.idReception


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
    regdate = models.DateTimeField('Regdate', default=datetime.now(), editable=False)

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


