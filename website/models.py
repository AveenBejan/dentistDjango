
from django.db import models
from django.conf import settings


class WebsiteFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField()  # Assuming 1-5 star rating
    comment = models.TextField(blank=True)

    # Additional fields like timestamp, IP address, etc., can be added for more information

    def __str__(self):
        return f"Rating: {self.rating}, User: {self.user.username if self.user else 'Anonymous'}"


class BasicInfo(models.Model):
    fullname = models.CharField('fullname',max_length=120)
    gender = models.CharField('Gender', max_length=20)
    phoneNumber = models.CharField('phoneNumber',max_length=120)
    address = models.CharField('address',max_length=120)
    type = models.CharField('type',max_length=120)
    startDay = models.DateField()
    salaryPaid = models.DecimalField('salaryPaid', max_digits=8, decimal_places=0, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True, editable=False)


class Salary(models.Model):
    idBasicInfo = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, blank=True,null=True)
    fullname = models.CharField('fullname',max_length=120)
    salaryPaid = models.DecimalField('salaryPaid',max_digits=8,decimal_places=0,null=False)
    days = models.IntegerField('days')
    finalSalary = models.DecimalField('finalSalary',max_digits=8,decimal_places=0,null=False)
    regdate = models.DateTimeField('Regdate', auto_now_add=True, editable=False)
    month = models.CharField('Month',null=True,max_length=120)  # Add a month field

    def __str__(self):
        return self.fullname  # You can customize this based on your needs


class Outcome(models.Model):
    invoice_num = models.CharField('fullname',max_length=120)
    invoice_date = models.DateField(null=True)
    type = models.CharField('fullname',max_length=120)
    description = models.CharField('fullname',max_length=120)
    price = models.DecimalField('finalSalary',max_digits=8,decimal_places=0,null=False)
    regdate = models.DateTimeField('Regdate', auto_now_add=True, editable=False)


class Doctors(models.Model):
    doctor_name = models.CharField('doctor_name',max_length=120)
    phone = models.CharField('phone',max_length=120)
    gender = models.CharField('Gender',max_length=20)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)

    def __str__(self):
        return self.doctor_name


class Educational(models.Model):
    educational_name = models.CharField('educational_name',max_length=120)
    phone = models.CharField('phone',max_length=120)
    gender = models.CharField('Gender',max_length=20)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)

    def __str__(self):
        return self.educational_name


class Reception(models.Model):
    name = models.CharField('Name',max_length=120)
    phone = models.CharField('phone',max_length=120)
    gender = models.CharField('Gender',max_length=20)
    date_of_birth = models.DateField(null=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True,null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    app_data = models.DateField(null=True)
    days = models.CharField('Days',max_length=20,null=True)
    time = models.CharField(null=True,max_length=200)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)

    def __str__(self):
        return self.name


class GaveAppointment(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField('Name',max_length=120,null=True)
    phone = models.CharField('Phone', max_length=120,null=True)
    gender = models.CharField('Gender', max_length=20,null=True)
    date_of_birth = models.CharField('date_of_birth', max_length=20,null=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True,null=True)
    app_data = models.DateField(null=True)
    days = models.CharField('Days', max_length=20, null=True)
    time = models.CharField(null=True, max_length=200)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)


class Filling(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True,null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('date_of_birth', max_length=20,null=False)
    filling_type = models.CharField('filling_type', max_length=120, blank=True,null=False)
    fillingur1 = models.CharField('filling_place',max_length=120, blank=True,null=True)
    fillingur2 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingur3 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingur4 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingur5 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingur6 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingur7 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingur8 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul1 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul2 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul3 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul4 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul5 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul6 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul7 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingul8 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr1 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr2 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr3 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr4 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr5 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr6 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr7 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillinglr8 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll1 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll2 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll3 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll4 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll5 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll6 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll7 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    fillingll8 = models.CharField('filling_place', max_length=120, blank=True, null=True)
    ur = models.CharField('ur', max_length=120, blank=True,null=True)
    ul = models.CharField('ul', max_length=120, blank=True,null=True)
    lr = models.CharField('lr', max_length=120,null=True, blank=True)
    ll = models.CharField('ll', max_length=120,null=True, blank=True)
    no_prepare = models.IntegerField('no_prepare',blank=True,null=True)
    price = models.DecimalField('price',max_digits=8,decimal_places=0,null=False)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0, null=False)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True, null=True)
    note = models.CharField('Name', max_length=120, blank=True, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')


class Crown(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True, null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    shade = models.CharField('shade', max_length=120, blank=True,null=False)
    no_unite = models.CharField('no_unite',max_length=120, blank=True,null=False)
    color = models.CharField('color', max_length=120, blank=True,null=False)
    no_prepare = models.IntegerField('no_prepare',  blank=True,null=False)
    price = models.DecimalField('price',max_digits=8,decimal_places=0,null=False)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0,null=False)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True, null=True)
    note = models.CharField('Name', max_length=120, blank=True, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')


class Veneer(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True,null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    shade = models.CharField('shade', max_length=120, blank=True,null=False)
    no_unite = models.CharField('no_unite',max_length=120, blank=True,null=False)
    color = models.CharField('color', max_length=120, blank=True,null=False)
    no_prepare = models.IntegerField('no_prepare', blank=True,null=False)
    price = models.DecimalField('price',max_digits=8,decimal_places=0,null=False)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0,null=False)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True, null=True)
    note = models.CharField('Name', max_length=120, blank=True, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')


class Endo(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True,null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('date_of_birth', max_length=20,null=False)
    first_visit = models.DateField('date_of_birth', max_length=20, blank=True,null=True)
    components_first = models.CharField('components', max_length=120, blank=True,null=True)
    ur = models.CharField('ur', max_length=120, blank=True,null=True)
    ul = models.CharField('ul', max_length=120, blank=True,null=True)
    lr = models.CharField('lr', max_length=120,null=True, blank=True)
    ll = models.CharField('ll', max_length=120,null=True, blank=True)
    canal = models.CharField('canal', max_length=120, blank=True, null=True)
    work_length = models.CharField('work_length', max_length=120, blank=True, null=True)
    no_prepare = models.IntegerField('no_prepare',null=True,blank=True)
    price = models.DecimalField('price',max_digits=8,decimal_places=0,null=False)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0, null=False)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True, null=True)
    note = models.CharField('Name', max_length=120, blank=True, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')
    second_visit = models.DateField(blank=True, null=True)
    components_second = models.CharField('components_second', max_length=120, blank=True, null=True)
    third_visit = models.DateField(blank=True, null=True)
    components_third = models.CharField('components_third', max_length=120, blank=True, null=True)
    fourth_visit = models.DateField(blank=True, null=True)
    components_fourth = models.CharField('components_fourth', max_length=120, blank=True, null=True)


class Medicine1(models.Model):
    name_medicine = models.CharField(max_length=120)

    def __str__(self):
        return self.name_medicine


class UploadedFile(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')


class Drug(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True,null=False)
    name_medicine = models.CharField(max_length=200, blank=True,null=False)  # This should be a CharField, not ForeignKey
    name = models.CharField('Name', max_length=120,blank=True,null=False)
    phone = models.CharField('Phone', max_length=120,blank=True,null=False)
    gender = models.CharField('Gender', max_length=20,blank=True,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,blank=True,null=False)
    doze = models.CharField(max_length=200,blank=True,null=True)
    type = models.CharField(max_length=200,blank=True,null=True)
    times = models.CharField(max_length=200,blank=True,null=True)
    tablet = models.CharField(max_length=200, blank=True, null=True)
    dispense = models.CharField(max_length=200, blank=True, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True, editable=False)


class Exo(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True, null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    ur = models.CharField('Name',max_length=120, blank=True,null=True)
    ul = models.CharField('Name', max_length=120, blank=True,null=True)
    lr = models.CharField('Name', max_length=120, blank=True,null=True)
    ll = models.CharField('Name', max_length=120, blank=True,null=True)
    price = models.DecimalField('price',max_digits=20,decimal_places=0,null=True)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0, null=True)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True,null=True)
    note = models.CharField('Name', max_length=120, blank=True,null=True)
    exoby = models.CharField('Name', max_length=120, blank=True,null=True)
    simpleexo = models.CharField('Name', max_length=120, blank=True,null=True)
    complcated = models.CharField('Name', max_length=120, blank=True,null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')

    def __str__(self):
        return self.name


class Implant(models.Model):
    implant_name = models.CharField('implant_name',max_length=120)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)

    def __str__(self):
        return self.implant_name


class OralSurgery(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE,blank=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True, null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120, blank=True,null=True)
    phone = models.CharField('Phone', max_length=120, blank=True,null=True)
    gender = models.CharField('Gender', max_length=20, blank=True,null=True)
    date_of_birth = models.CharField('Gender', max_length=20, blank=True,null=True)
    implant = models.ForeignKey(Implant, on_delete=models.CASCADE, blank=True,null=True)
    diameterur1 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur1 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterur2 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur2 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterur3 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur3 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterur4 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur4 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterur5 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur5 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterur6 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur6 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterur7 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur7 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterur8 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthur8 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterul1 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthul1 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterul2 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthul2 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterul3 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthul3 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterul4 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthul4 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterul5 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthul5 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterul6 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthul6 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterul7 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthul7 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterul8 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthul8 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterlr1 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthlr1 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterlr2 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthlr2 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterlr3 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthlr3 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterlr4 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthlr4 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterlr5 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthlr5 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterlr6 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthlr6 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterlr7 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthlr7 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterlr8 = models.CharField('Diameter', max_length=20, blank=True, null=True)
    lengthlr8 = models.CharField('Length', max_length=20, blank=True, null=True)
    diameterll1 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll1 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterll2 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll2 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterll3 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll3 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterll4 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll4 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterll5 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll5 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterll6 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll6 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterll7 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll7 = models.CharField('Length',max_length=20, blank=True,null=True)
    diameterll8 = models.CharField('Diameter',max_length=20, blank=True,null=True)
    lengthll8 = models.CharField('Length',max_length=20, blank=True,null=True)
    no_Implant = models.CharField('No_Implant',max_length=120,blank=True)
    ur = models.CharField('Name',max_length=120, blank=True,null=True)
    ul = models.CharField('Name', max_length=120, blank=True,null=True)
    lr = models.CharField('Name', max_length=120, blank=True,null=True)
    ll = models.CharField('Name', max_length=120, blank=True,null=True)
    color = models.CharField('color', max_length=20, blank=True, null=True)
    shade = models.CharField('shade', max_length=120, blank=True,null=True)
    no_unite = models.IntegerField('no_unite', blank=True,null=True)
    no_prepare = models.IntegerField('no_prepare',  blank=True,null=True)
    price = models.DecimalField('price',max_digits=8,decimal_places=0,null=True)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0,null=True)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True,null=True)
    date = models.DateField(blank=True, null=True)
    note = models.CharField('Name', max_length=120, blank=True, null=True)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')
    first_visit = models.DateField(blank=True,null=True)
    second_visit = models.DateField(blank=True,null=True)
    third_visit = models.DateField(blank=True,null=True)
    fourth_visit = models.DateField(blank=True,null=True)
    fifth_visit = models.DateField(blank=True,null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)

    def __str__(self):
        return self.idReception


class Visits(models.Model):
    visit_name = models.CharField('visit_name',max_length=120, blank=True,null=True)
    regdate = models.DateTimeField('Regdate',auto_now_add=True,editable=False)

    def __str__(self):
        return self.visit_name


class Periodontology(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True, null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    type = models.CharField('Name',max_length=120, blank=True,null=True)
    price = models.DecimalField('price',max_digits=20,decimal_places=0,null=True)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0, null=True)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True, null=True)
    note = models.CharField('Name', max_length=120, blank=True, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')


class Prosthodontics(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE, blank=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True, null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120,null=False)
    phone = models.CharField('Phone', max_length=120,null=False)
    gender = models.CharField('Gender', max_length=20,null=False)
    date_of_birth = models.CharField('Gender', max_length=20,null=False)
    ur = models.CharField('Name',max_length=120, blank=True,null=True)
    ul = models.CharField('Name', max_length=120, blank=True,null=True)
    lr = models.CharField('Name', max_length=120, blank=True,null=True)
    ll = models.CharField('Name', max_length=120, blank=True,null=True)
    price = models.DecimalField('price',max_digits=20,decimal_places=0,null=True)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0, null=True)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, null=True)
    date = models.DateField(blank=True, null=True)
    note = models.CharField('Name', max_length=120, blank=True, null=True)
    denture = models.CharField('Name', max_length=120, blank=True,null=True)
    upper = models.CharField('Name', max_length=120, blank=True, null=True)
    lower = models.CharField('Name', max_length=120, blank=True, null=True)
    partial = models.CharField('Name', max_length=120, blank=True, null=True)
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    exo_images = models.ImageField(null=True, blank=True,upload_to='')

    def __str__(self):
        return self.name


class Ortho(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE,blank=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, blank=True,null=True)
    educational = models.ForeignKey(Educational, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Name',max_length=120, blank=True,null=True)
    phone = models.CharField('Phone', max_length=120, blank=True,null=True)
    gender = models.CharField('Gender', max_length=20, blank=True,null=True)
    date_of_birth = models.CharField('Gender', max_length=20, blank=True,null=True)
    ur = models.CharField('Name',max_length=120, blank=True,null=True)
    ul = models.CharField('Name', max_length=120, blank=True,null=True)
    lr = models.CharField('Name', max_length=120, blank=True,null=True)
    ll = models.CharField('Name', max_length=120, blank=True,null=True)
    urn = models.CharField('Name',max_length=120, blank=True,null=True)
    uln = models.CharField('Name', max_length=120, blank=True,null=True)
    lrn = models.CharField('Name', max_length=120, blank=True,null=True)
    lln = models.CharField('Name', max_length=120, blank=True,null=True)
    teeth_type = models.CharField('teeth_type', max_length=120, blank=True,null=True)
    angle_class = models.CharField('angle_class', max_length=120, blank=True,null=True)
    over_jet = models.CharField('Name', max_length=120, blank=True,null=True)
    over_bt = models.CharField('Name', max_length=120, blank=True,null=True)
    jow_shift = models.CharField('Name', max_length=120, blank=True,null=True)
    midlin_shift = models.CharField('Name', max_length=120, blank=True,null=True)
    urs = models.CharField('Name',max_length=120, blank=True,null=True)
    uls = models.CharField('Name', max_length=120, blank=True,null=True)
    lrs = models.CharField('Name', max_length=120, blank=True,null=True)
    lls = models.CharField('Name', max_length=120, blank=True,null=True)
    teeth_size = models.CharField('Name', max_length=120, blank=True,null=True)
    SNA_before = models.CharField('Name', max_length=120, blank=True,null=True)
    SNA_after = models.CharField('Name', max_length=120, blank=True,null=True)
    SNB_before = models.CharField('Name', max_length=120, blank=True,null=True)
    SNB_after = models.CharField('Name', max_length=120, blank=True,null=True)
    ANB_before = models.CharField('Name', max_length=120, blank=True,null=True)
    ANB_after = models.CharField('Name', max_length=120, blank=True,null=True)
    IMPA_before = models.CharField('Name', max_length=120, blank=True,null=True)
    IMPA_after = models.CharField('Name', max_length=120, blank=True,null=True)
    U1_SN_before = models.CharField('Name', max_length=120, blank=True,null=True)
    U1_SN_after = models.CharField('Name', max_length=120, blank=True,null=True)
    SNGOGN_before = models.CharField('Name', max_length=120, blank=True,null=True)
    SNGOGN_after = models.CharField('Name', max_length=120, blank=True,null=True)
    treatment_plan = models.CharField('Name', max_length=245, blank=True,null=True)
    visits = models.ForeignKey(Visits, on_delete=models.CASCADE, blank=True,null=True)
    wive_size = models.CharField('Name', max_length=120, blank=True,null=True)
    cross_sectional = models.CharField('Name', max_length=120, blank=True,null=True)
    material = models.CharField('Name', max_length=120, blank=True,null=True)
    brackets = models.CharField('Name', max_length=120, blank=True, null=True)
    price = models.DecimalField('price',max_digits=8,decimal_places=0,blank=True,null=True)
    total_price = models.DecimalField('price', max_digits=20, decimal_places=0, null=True)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0, blank=True,null=True)
    date = models.DateField(blank=True, null=True)
    notes = models.CharField('Name', max_length=120, blank=True, null=True)
    exo_images = models.ImageField(null=True, blank=True, upload_to='')
    regdate = models.DateTimeField('Regdate', auto_now_add=True,editable=False)
    visit_date = models.DateField('Visit Date', null=True, blank=True)

    def __str__(self):
        return self.idReception


class Photo(models.Model):
    exo_instance = models.ForeignKey(Exo, on_delete=models.CASCADE,null=True)
    crown_instance = models.ForeignKey(Crown, on_delete=models.CASCADE,null=True)
    veneer_instance = models.ForeignKey(Veneer, on_delete=models.CASCADE, null=True)
    filling_instance = models.ForeignKey(Filling, on_delete=models.CASCADE, null=True)
    oral_surgery_instance = models.ForeignKey(OralSurgery, on_delete=models.CASCADE, null=True)
    endo_instance = models.ForeignKey(Endo, on_delete=models.CASCADE, null=True)
    ortho_instance = models.ForeignKey(Ortho, on_delete=models.CASCADE, null=True)
    periodontology_instance = models.ForeignKey(Periodontology, on_delete=models.CASCADE, null=True)
    prosthodontics_instance = models.ForeignKey(Prosthodontics, on_delete=models.CASCADE, null=True)
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


class Debts(models.Model):
    idReception = models.ForeignKey(Reception, on_delete=models.CASCADE)
    idExo = models.ForeignKey(Exo, on_delete=models.CASCADE)
    idFilling = models.ForeignKey(Filling, on_delete=models.CASCADE)
    idCrown = models.ForeignKey(Crown, on_delete=models.CASCADE)
    idVeneer = models.ForeignKey(Veneer, on_delete=models.CASCADE)
    idOralSurgery = models.ForeignKey(OralSurgery, on_delete=models.CASCADE)
    totalPrice = models.DecimalField('totalPrice', max_digits=20, decimal_places=0,null=True)
    paid = models.DecimalField('paid', max_digits=20, decimal_places=0,null=True)
    remaining = models.DecimalField('remaining', max_digits=20, decimal_places=0,null=True)
    regDate = models.DateTimeField('RegDate', auto_now_add=True, editable=False)

    def __str__(self):
        return f"Debt for Reception: {self.idReception}, Remaining: {self.remaining}"


