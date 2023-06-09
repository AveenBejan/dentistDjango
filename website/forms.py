from django import forms
from django.forms import ModelForm
from .models import Contact, Appointment1,DentistDetails,Reception,OralSurgery, Orthodontics


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


class ReceptionForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = ('name','phone')
        labels = {
            'name': '',
            'phone': '',
        }
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
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

