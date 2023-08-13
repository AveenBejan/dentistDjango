from django import forms
from django.forms import ModelForm
from .models import Contact, Appointment1,DentistDetails,Reception,OralSurgery, Orthodontics,Exo,Medicin,Photo,Drug,\
    Crown,Medicine1,Veneer,Filling,Doctors
from django.forms import formset_factory


class DoctorsForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ( 'doctor_name', 'phone', 'gender')
        labels = {
            'doctor_name': '',
            'phone': '',
            'gender': '',

        }
        widgets = {
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'doctor_name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
        }


class ReceptionForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Select Doctor", to_field_name='doctor_name')
    class Meta:
        model = Reception
        fields = ('name', 'phone', 'gender', 'date_of_birth', 'doctor','app_data','days', 'time')
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number',
            'gender': 'Gender',
            'date_of_birth': 'Date of Birth',
            'doctor': '',
            'app_data': '',
            'days': '',
            'time': 'Time',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'app_data': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'days': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Appointment Time'}),
        }


class SearchForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Select Doctor")


class Medicine1Form(forms.ModelForm):
    class Meta:
        model = Medicine1
        fields = ['name_medicine']
        labels = {
            'name_medicine': '',}
        widgets = {
            'name_medicine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),}


class DrugForm(forms.ModelForm):
    name_medicine = forms.ModelChoiceField(queryset=Medicine1.objects.all(),widget=forms.Select(attrs=
                                           {'class': 'form-control'}), empty_label='Select Medicine')

    TYPE_CHOICES = [
        ('', 'Select Type'),
        ('mg', 'mg'),
        ('g', 'g'),
    ]
    TIMES_CHOICES = [
        ('', 'Select Times'),
        ('1*1', '1*1'),
        ('1*2', '1*2'),
        ('1*3', '1*3'),
        ('1*4', '1*4'),
        ('1*5', '1*5'),
        ('1*6', '1*6'),
    ]

    type = forms.ChoiceField(choices=TYPE_CHOICES, initial='', widget=forms.Select(attrs={'class': 'form-control'}))
    times = forms.ChoiceField(choices=TIMES_CHOICES, initial='',
                              widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Drug
        fields = ['idReception', 'name', 'phone', 'gender', 'date_of_birth', 'name_medicine', 'doze', 'type', 'times']
        labels = {
            'idReception': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'name_medicine': '',
            'doze': '',
            'type': '',
            'times': '',
        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'type': 'hidden'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone', 'type': 'hidden'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender', 'type': 'hidden'}),
            'date_of_birth': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'date_of_birth', 'type': 'hidden'}),
            'name_medicine': forms.Select(attrs={'class': 'form-control', 'placeholder': 'name_medicine'}),
            'doze': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'doze'}),
        }


DrugFormSet = formset_factory(DrugForm, extra=5)  # Set `extra` to the number of forms you want to display initially.


class MedicinForm(forms.ModelForm):
    class Meta:
        model = Medicin
        fields = ('idReception', 'name', 'phone', 'gender', 'date_of_birth', 'antibiotic', 'analogous', 'mouthwash')
        labels = {
            'idReception': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'antibiotic': '',
            'analogous': '',
            'mouthwash': '',


        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'antibiotic': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'antibiotic'}),
            'analogous': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'analogous'}),
            'mouthwash': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'mouthwash'}),

        }


class FillingForm(forms.ModelForm):
    exo_images = forms.FileInput()

    class Meta:
        model = Filling
        fields = ('idReception', 'name', 'phone', 'gender', 'date_of_birth','filling_type','filling_place',
                  'ur', 'ul', 'lr', 'll',  'no_prepare', 'price', 'note','exo_images')
        labels = {
            'idReception': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'filling_type': '',
            'filling_place': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'no_prepare': '',
            'price': '',
            'note': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'filling_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'filling_type'}),
            'filling_place': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),

        }


class ExoForm(forms.ModelForm):
    exo_images = forms.FileInput()

    class Meta:
        model = Exo
        fields = ('idReception', 'name', 'phone', 'gender', 'date_of_birth','ur', 'ul', 'lr', 'll','no_prepare', 'price', 'note', 'exoby', 'simpleexo', 'complcated','exo_images')
        labels = {
            'idReception': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'no_prepare': '',
            'price': '',
            'note': '',
            'exoby': '',
            'simpleexo': '',
            'complcated': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'exoby': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'exoby'}),
            'simpleexo': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'simpleexo'}),
            'complcated': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'placeholder': 'complcated'}),

        }


class CrownForm(forms.ModelForm):
    exo_images = forms.FileInput()

    class Meta:
        model = Crown
        fields = ('idReception', 'name', 'phone', 'gender', 'date_of_birth','shade', 'no_unite', 'color', 'no_prepare', 'price', 'note', 'exo_images')
        labels = {
            'idReception': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'shade': '',
            'no_unite': '',
            'color': '',
            'no_prepare': '',
            'price': '',
            'note': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'shade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'shade'}),
            'no_unite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_unite'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'color'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),

        }


class VeneerForm(forms.ModelForm):
    exo_images = forms.FileInput()

    class Meta:
        model = Veneer
        fields = ('idReception', 'name', 'phone', 'gender', 'date_of_birth','shade', 'no_unite', 'color', 'no_prepare', 'price', 'note', 'exo_images')
        labels = {
            'idReception': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'shade': '',
            'no_unite': '',
            'color': '',
            'no_prepare': '',
            'price': '',
            'note': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'shade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'shade'}),
            'no_unite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_unite'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'color'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),

        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']


class OralSurgeryForm(forms.ModelForm):
    class Meta:
        model = OralSurgery
        fields = ('idReception','tooth', 'RX', 'material_type', 'thickness_rich', 'size', 'size_direction', 'size_number', 'second_visit', 'third_visit', 'fourth_visit', 'fifth_visit')
        labels = {
            'idReception': '',
            'tooth': '',
            'RX': '',
            'material_type': '',
            'thickness_rich': '',
            'size': '',
            'size_direction': '',
            'size_number': '',
            'second_visit': '',
            'third_visit': '',
            'fourth_visit': '',
            'fifth_visit': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'tooth': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Tooth Extraction'}),
            'RX': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'size'}),
            'material_type': forms.RadioSelect(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'thickness_rich': forms.RadioSelect(attrs={'class': 'form-control', 'placeholder': 'thickness_rich'}),
            'size': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'size'}),
            'size_direction': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'size_direction'}),
            'size_number': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'size_number'}),
            'second_visit': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'placeholder': 'second_visit'}),
            'third_visit': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'third_visit'}),
            'fourth_visit': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'fourth_visit'}),
            'fifth_visit': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'fifth_visit'}),
        }




class DentistDetailsForm(forms.ModelForm):
    class Meta:
        model = DentistDetails
        fields = ('idappointment','details', 'medicine_name','medicine_time','medicine_period', 'medicine_tfood','medicine_no')
        labels = {
            'idappointment': '',
            'details': '',
            'medicine_name': '',
            'medicine_time': '',
            'medicine_period': '',
            'medicine_tfood': '',
            'medicine_no': '',
        }
        widgets = {
            'idappointment': forms.Select(attrs={'class': 'form-control'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'details'}),
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'medicine_name'}),
            'medicine_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'medicine_time'}),
            'medicine_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'medicine_period'}),
            'medicine_tfood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'medicine_tfood'}),
            'medicine_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'medicine_no'}),
        }


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        labels = {
            'name': '',
            'email': '',
            'subject': '',
            'message': '',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message'}),


        }


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment1
        fields = ('name', 'gender','birthday','email', 'address', 'date', 'phone')
        labels = {
            'name': '',
            'gender': '',
            'birthday': '',
            'email': '',
            'address': '',
            'date': '',
            'phone': '',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
            'birthday': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Birthday'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        }


class OrthodonticsForm(forms.ModelForm):
    YES_NO_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    MATERIAL_CHOICES = [('AUG', 'AUG'), ('AUG1', 'AUG1')]
    WIDTH_CHOICES = [('3*10', '3*10'), ('4*10', '4*10')]

    name = forms.CharField(label='Name', max_length=100)
    yes_no_field = forms.ChoiceField(label='Yes/No', choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    material_field = forms.MultipleChoiceField(label='Material', choices=MATERIAL_CHOICES, widget=forms.CheckboxSelectMultiple)
    width_field = forms.MultipleChoiceField(label='Width', choices=WIDTH_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Orthodontics
        fields = ('name', 'yes_no_field', 'material_field', 'width_field')

