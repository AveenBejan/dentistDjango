from django import forms
from django.forms import ModelForm
from .models import Contact, Appointment1,DentistDetails,Reception,OralSurgery, Ortho,Exo,Medicin,Photo,Drug,\
    Crown,Medicine1,Veneer,Filling,Doctors,Implant,GaveAppointment,Debts, BasicInfo,Salary,Outcome,Endo,\
    Visits,Educational,Periodontology,Prosthodontics,UploadedFile,WebsiteFeedback,PaymentHistory,Reception1,Pedo,Store,Material,Lab,MaterialOutput,Xrays,Surgery,Preventive,Diagnosis
from django.forms import formset_factory


class DiagnosisForm(forms.ModelForm):

    class Meta:
        model = Diagnosis
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth',
                  'ur1', 'ul1', 'lr1', 'll1',
                  'ur2', 'ul2', 'lr2', 'll2',
                  'ur3', 'ul3', 'lr3', 'll3',
                  'type',
                  'ur5', 'ul5', 'lr5', 'll5',
                  'ur6', 'ul6', 'lr6', 'll6',
                  'ur7', 'ul7', 'lr7', 'll7',
                  'ur8', 'ul8', 'lr8', 'll8',
                  'ur9', 'ul9', 'lr9', 'll9',
                  'ur10', 'ul10', 'lr10', 'll10',
                  'ur11', 'ul11', 'lr11', 'll11',
                  'ur12', 'ul12', 'lr12', 'll12','price',
                  'note1','note2','note3','note4','note5','note6','note6','note7','note8','note9','note10','note11','note12')
        labels = {
            'idReception1': '',
            'idReception': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur1': '',
            'ul1': '',
            'lr1': '',
            'll1': '',
            'price': '',
            'note': '',

        }
        widgets = {
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'type': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),

        }


class WebsiteFeedbackForm(forms.ModelForm):
    class Meta:
        model = WebsiteFeedback
        fields = ['rating', 'comment']
        # You can also include additional fields if required

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customization for fields (if needed)
        self.fields['rating'].widget = forms.NumberInput(attrs={'min': '1', 'max': '5'})  # Adjusts the input for rating
        self.fields['comment'].widget = forms.Textarea(attrs={'rows': 4})  # Adjusts the textarea size


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['pdf_file']


class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ('invoice_num', 'invoice_date', 'type', 'description', 'price')
        labels = {
            'invoice_num': '',
            'invoice_date': '',
            'type': '',
            'description': '',
            'price': '',

        }
        widgets = {
            'invoice_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'invoice_num'}),
            'invoice_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'invoice_date'}),
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'type'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
        }


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = BasicInfo
        fields = ( 'fullname', 'gender', 'phoneNumber','address', 'type', 'startDay','salaryPaid')
        labels = {
            'fullname': '',
            'gender': '',
            'phoneNumber': '',
            'address': '',
            'type': '',
            'startDay': '',
            'salaryPaid': '',

        }
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fullname'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phoneNumber'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'type'}),
            'startDay': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'startDay'}),
            'salaryPaid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'salaryPaid'}),
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ('idBasicInfo', 'fullname', 'salaryPaid', 'days', 'month')
        labels = {
            'idBasicInfo': '',
            'fullname': '',
            'salaryPaid': '',
            'days': '',
            'month': '',
        }
        widgets = {
            'idBasicInfo': forms.Select(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fullname'}),
            'salaryPaid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'salaryPaid'}),
            'days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'days'}),
            'month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'days'}),

        }


class DoctorsForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ( 'doctor_name', 'phone', 'gender', 'proportion_doctor', 'proportion_center', 'salary')
        labels = {
            'doctor_name': '',
            'phone': '',
            'gender': '',
            'proportion_doctor': '',
            'proportion_center': '',
            'salary': '',


        }
        widgets = {
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'doctor_name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'proportion_doctor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'proportion_center': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('material_name',)
        labels = {
            'material_name': '',
        }
        widgets = {
            'material_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'doctor_name'}),
        }


class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ('lab_name',)
        labels = {
            'lab_name': '',
        }
        widgets = {
            'lab_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'doctor_name'}),
        }


class EducationalForm(forms.ModelForm):
    class Meta:
        model = Educational
        fields = ( 'educational_name', 'phone', 'gender')
        labels = {
            'educational_name': '',
            'phone': '',
            'gender': '',

        }
        widgets = {
            'educational_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'educational_name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
        }


class GaveAppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Select Doctor",to_field_name='doctor_name')

    class Meta:
        model = GaveAppointment
        fields = ( 'name', 'phone', 'gender', 'date_of_birth','doctor','app_data','days', 'time')
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number',
            'gender': 'Gender',
            'date_of_birth': 'Date of Birth',
            'doctor': '',

            'app_data':'',
            'days': '',
            'time': 'Time',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'app_data': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'days': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Appointment Time'}),
        }


class ReceptionForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), to_field_name='doctor_name')
    educational = forms.ModelChoiceField(queryset=Educational.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}),
                                         to_field_name='educational_name', required=False)
    GENDER_CHOICES = (
        ('', '----------'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reception
        fields = ('name', 'phone', 'gender', 'date_of_birth', 'doctor','educational','app_data','days', 'time','user','note')
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number',
            'gender': 'Gender',
            'date_of_birth': 'Date of Birth',
            'doctor': '',
            'educational': '',
            'app_data': '',
            'days': '',
            'time': 'Time',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),

            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'app_data': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'days': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Appointment Time'}),
        }


class ReceptionForm1(forms.ModelForm):
    class Meta:
        model = Reception1
        fields = ('idReception','name', 'phone', 'gender', 'date_of_birth', 'doctor','educational','app_data','days', 'time','user','note')
        labels = {
            'idReception': 'idReception',
            'name': 'Full Name',
            'phone': 'Phone Number',
            'gender': 'Gender',
            'date_of_birth': 'Date of Birth',
            'doctor': '',
            'educational': '',
            'app_data': '',
            'days': '',
            'time': 'Time',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'app_data': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'days': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Appointment Time'}),
        }


class SearchForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Select Doctor", required=False)


class SearchForm1(forms.Form):
    educational = forms.ModelChoiceField(queryset=Educational.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Select Educational Center")


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
                                           {'class': 'form-control'}), empty_label='Select Drugs', required=True)

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
    TABLET_CHOICES = [
        ('', 'Select Tablet'),
        ('Tablet', 'Tablet'),
        ('Syrup', 'Syrup'),
        ('Ointment', 'Ointment'),
        ('Mouth Wash', 'Mouth Wash'),
        ('Capsule', 'Capsule'),
        ('Drop', 'Drop'),
        ('Injection', 'Injection'),
        ('Jel', 'Jel'),
    ]
    DISPENSE_CHOICES = [
        ('', 'Select Dispense'),
        ('1 Day', '1 Day'),
        ('2 Days', '2 Days'),
        ('3 Days', '3 Days'),
        ('4 Days', '4 Days'),
        ('5 Days', '5 Days'),
        ('6 Days', '6 Days'),
        ('7 Days', '7 Days'),
        ('One Week', 'One Week'),
        ('Two Weeks', 'Two Week'),
    ]

    type = forms.ChoiceField(choices=TYPE_CHOICES, initial='', widget=forms.Select(attrs={'class': 'form-control'}),
                             required=True)
    times = forms.ChoiceField(choices=TIMES_CHOICES, initial='',widget=forms.Select(attrs={'class': 'form-control'}),
                              required=True)
    tablet = forms.ChoiceField(choices=TABLET_CHOICES, initial='',widget=forms.Select(attrs={'class': 'form-control'}),
                               required=True)
    dispense = forms.ChoiceField(choices=DISPENSE_CHOICES, initial='',widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Drug
        fields = ['idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth', 'name_medicine', 'doze', 'type', 'times','tablet','dispense']
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'name_medicine': '',
            'doze': '',
            'type': '',
            'times': '',
            'tablet': '',
            'dispense': '',
        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'}),
            'idReception1': forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'}),
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
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)

    class Meta:
        model = Filling
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','filling_type','fillingur1','fillingur2','fillingur3','fillingur4','fillingur5','fillingur6','fillingur7',
                  'fillingur8','fillingul1','fillingul2','fillingul3','fillingul4','fillingul5','fillingul6','fillingul7',
                  'fillingul8','fillinglr1','fillinglr2','fillinglr3','fillinglr4','fillinglr5','fillinglr6','fillinglr7',
                  'fillinglr8','fillingll1','fillingll2','fillingll3','fillingll4','fillingll5','fillingll6','fillingll7',
                  'fillingll8',
                  'ur', 'ul', 'lr', 'll',  'no_prepare', 'price','paid','date', 'note','exo_images','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'filling_type': '',
            'fillingur1': '',
            'fillingur2': '',
            'fillingur3': '',
            'fillingur4': '',
            'fillingur5': '',
            'fillingur6': '',
            'fillingur7': '',
            'fillingur8': '',
            'fillingul1': '',
            'fillingul2': '',
            'fillingul3': '',
            'fillingul4': '',
            'fillingul5': '',
            'fillingul6': '',
            'fillingul7': '',
            'fillingul8': '',
            'fillinglr1': '',
            'fillinglr2': '',
            'fillinglr3': '',
            'fillinglr4': '',
            'fillinglr5': '',
            'fillinglr6': '',
            'fillinglr7': '',
            'fillinglr8': '',
            'fillingll1': '',
            'fillingll2': '',
            'fillingll3': '',
            'fillingll4': '',
            'fillingll5': '',
            'fillingll6': '',
            'fillingll7': '',
            'fillingll8': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'no_prepare': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'filling_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'filling_type'}),
            'fillingur1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingur2': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingur3': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingur4': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingur5': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingur6': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingur7': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingur8': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul2': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul3': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul4': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul5': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul6': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul7': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingul8': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr2': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr3': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr4': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr5': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr6': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr7': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglr8': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll1': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll2': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll3': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll4': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll5': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll6': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll7': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingll8': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),

        }


class PedoForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)

    class Meta:
        model = Pedo
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','filling_type','fillingurA','fillingurB','fillingurC','fillingurD','fillingurE','fillingulA','fillingulB','fillingulC','fillingulD','fillingulE','fillinglrA','fillinglrB','fillinglrC','fillinglrD','fillinglrE',
                  'fillingllA','fillingllB','fillingllC','fillingllD','fillingllE',
                  'ur', 'ul', 'lr', 'll',  'no_prepare', 'price','paid','date', 'note','exo_images','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'filling_type': '',
            'fillingurA': '',
            'fillingurB': '',
            'fillingurC': '',
            'fillingurD': '',
            'fillingurE': '',
            'fillingulA': '',
            'fillingulB': '',
            'fillingulC': '',
            'fillingulD': '',
            'fillingulE': '',
            'fillinglrA': '',
            'fillinglrB': '',
            'fillinglrC': '',
            'fillinglrD': '',
            'fillinglrE': '',
            'fillingllA': '',
            'fillingllB': '',
            'fillingllC': '',
            'fillingllD': '',
            'fillingllE': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'no_prepare': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',


        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'filling_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'filling_type'}),
            'fillingurA': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingurB': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingurC': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingurD': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingurE': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingulA': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingulB': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingulC': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingulD': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingulE': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglrA': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglrB': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglrC': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglrD': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillinglrE': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingllA': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingllB': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingllC': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingllD': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'fillingllE': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'filling_place'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),

        }


class ExoForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label='Select Lab', required=False)

    class Meta:
        model = Exo
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','ur', 'ul', 'lr', 'll', 'price',
                  'paid','date', 'note', 'exoby', 'simpleexo', 'complcated','exo_images', 'discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception1': '',
            'idExo': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',

            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'exoby': '',
            'simpleexo': '',
            'complcated': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',



        }
        widgets = {
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'idExo': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),

            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'exoby': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'exoby'}),
            'simpleexo': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'simpleexo'}),
            'complcated': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'placeholder': 'complcated'}),


        }


class SurgeryForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label='Select Lab', required=False)

    class Meta:
        model = Surgery
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','ur', 'ul', 'lr', 'll', 'price',
                  'paid','date', 'note','exo_images', 'discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception1': '',
            'idExo': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',



        }
        widgets = {
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'idExo': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),

            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }


class PreventiveForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label='Select Lab', required=False)

    class Meta:
        model = Preventive
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','ur', 'ul', 'lr', 'll', 'price',
                  'paid','date', 'note','exo_images', 'discount_option','lab_name' ,'type_preventive',
                  'price_lab')
        labels = {
            'idReception1': '',
            'idExo': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',
            'type_preventive': '',



        }
        widgets = {
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'idExo': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),

            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'type_preventive': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
        }


class PeriodontologyForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)

    class Meta:
        model = Periodontology
        fields = ('idReception', 'idReception1', 'name', 'phone', 'gender', 'date_of_birth','type','price', 'paid', 'date', 'note', 'exo_images','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'type': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'type': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),

        }


class CrownForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)

    class Meta:
        model = Crown
        fields = ('idReception', 'idReception1', 'name', 'phone', 'gender', 'date_of_birth','shade', 'no_unite', 'color', 'no_prepare', 'price',  'paid','date', 'note', 'exo_images','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'shade': '',
            'no_unite': '',
            'color': '',
            'no_prepare': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'shade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'shade'}),
            'no_unite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_unite'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'color'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'discount_option': forms.Select(attrs={'class': 'form-control', 'placeholder': 'discount_option'}),

        }


class VeneerForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)

    class Meta:
        model = Veneer
        fields = ('idReception',  'idReception1', 'name', 'phone', 'gender', 'date_of_birth','shade', 'no_unite', 'color', 'no_prepare', 'price', 'paid', 'date', 'note', 'exo_images','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'shade': '',
            'no_unite': '',
            'color': '',
            'no_prepare': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'shade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'shade'}),
            'no_unite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_unite'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'color'}),
            'no_prepare': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_prepare'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),

        }


class ImplantForm(forms.ModelForm):
    class Meta:
        model = Implant
        fields = ['implant_name']
        labels = {
            'implant_name': '',}
        widgets = {
            'implant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'implant_name'}),}


class OralSurgeryForm(forms.ModelForm):
    exo_images = forms.FileInput()
    implant = forms.ModelChoiceField(queryset=Implant.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Select Implant",
                                    to_field_name='implant_name')
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label='Select Lab', required=False)

    class Meta:
        model = OralSurgery
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','implant',
                  'diameterur1', 'lengthur1', 'diameterur2', 'lengthur2', 'diameterur3', 'lengthur3', 'diameterur4', 'lengthur4',
                  'diameterur5', 'lengthur5', 'diameterur6', 'lengthur6', 'diameterur7', 'lengthur7', 'diameterur8', 'lengthur8',
                  'diameterul1', 'lengthul1', 'diameterul2', 'lengthul2', 'diameterul3', 'lengthul3', 'diameterul4', 'lengthul4',
                  'diameterul5', 'lengthul5', 'diameterul6', 'lengthul6', 'diameterul7', 'lengthul7', 'diameterul8', 'lengthul8',
                  'diameterlr1', 'lengthlr1', 'diameterlr2', 'lengthlr2', 'diameterlr3', 'lengthlr3', 'diameterlr4', 'lengthlr4',
                  'diameterlr5', 'lengthlr5', 'diameterlr6', 'lengthlr6', 'diameterlr7', 'lengthlr7', 'diameterlr8', 'lengthlr8',
                  'diameterll1', 'lengthll1', 'diameterll2', 'lengthll2', 'diameterll3', 'lengthll3', 'diameterll4', 'lengthll4',
                  'diameterll5', 'lengthll5', 'diameterll6', 'lengthll6', 'diameterll7', 'lengthll7', 'diameterll8', 'lengthll8',
                  'no_Implant', 'ur', 'ul','lr', 'll','shade','no_unite',
                  'color', 'price', 'paid','date', 'note', 'exo_images', 'first_visit','second_visit','third_visit',
                  'fourth_visit','fifth_visit' ,'discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '','idReception1': '','name': '','phone': '','gender': '','date_of_birth': '','first_visit': '','implant': '',
            'diameterur1': '', 'lengthur1': '','diameterur2': '', 'lengthur2': '','diameterur3': '','lengthur3': '', 'diameterur4': '', 'lengthur4': '',
            'diameterur5': '', 'lengthur5': '', 'diameterur6': '', 'lengthur6': '', 'diameterur7': '', 'lengthur7': '','diameterur8': '', 'lengthur8': '',
            'diameterul1': '', 'lengthul1': '','diameterul2': '', 'lengthul2': '', 'diameterul3': '', 'lengthul3': '', 'diameterul4': '','lengthul4': '',
            'diameterul5': '', 'lengthul5': '', 'diameterul6': '', 'lengthul6': '', 'diameterul7': '', 'lengthul7': '','diameterul8': '', 'lengthul8': '',
            'diameterlr1': '', 'lengthlr1': '', 'diameterlr2': '', 'lengthlr2': '', 'diameterlr3': '', 'lengthlr3': '', 'diameterlr4': '', 'lengthlr4': '',
            'diameterlr5': '', 'lengthlr5': '', 'diameterlr6': '', 'lengthlr6': '', 'diameterlr7': '', 'lengthlr7': '','diameterlr8': '', 'lengthlr8': '',
            'diameterll1': '', 'lengthll1': '','diameterll2': '', 'lengthll2': '', 'diameterll3': '', 'lengthll3': '', 'diameterll4': '', 'lengthll4': '',
            'diameterll5': '', 'lengthll5': '', 'diameterll6': '', 'lengthll6': '', 'diameterll7': '', 'lengthll7': '','diameterll8': '', 'lengthll8': '',
            'no_Implant': '',
            'no_unite': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'shade': '',
            'color': '',
            'price': '',
            'paid': '',
            'note': '',
    'date': '',
            'second_visit': '',
            'third_visit': '',
            'fourth_visit': '',
            'fifth_visit': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab':'',


        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'first_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'diameterur1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterur2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterur3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterur4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterur5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterur6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterur7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterur8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthur8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthu1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthul2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthul3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthul4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthu5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthul6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthul7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterul8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthul8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterlr8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthlr8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll6': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll7': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'diameterll8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'diameter'}),
            'lengthll8': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'material_type'}),
            'no_Implant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'no_Implant'}),
            'no_unite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'size'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'shade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'shade'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'color'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'second_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'third_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'fourth_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'fifth_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }


class EndoForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)

    class Meta:
        model = Endo
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','first_visit', 'components_first', 'ur', 'ul','lr', 'll','canal_b','work_length_b','canal_p','work_length_p',
                  'canal_mb','work_length_mb','canal_db','work_length_db','canal_p1','work_length_p1','canal_acc','work_length_acc','work_length_7','price', 'paid','date', 'note', 'exo_images', 'second_visit','components_second','third_visit', 'components_third', 'fourth_visit','components_fourth','filling_type','filling_type1','filling_type2','filling_type3','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'first_visit': '',
            'components_first': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'second_visit': '',
            'components_second': '',
            'third_visit': '',
            'components_third': '',
            'fourth_visit': '',
            'components_fourth': '',
            'filling_type': '',
            'filling_type1': '',
            'filling_type2': '',
            'filling_type3': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',



        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'first_visit': forms.DateInput(attrs={'class': 'form-control'}),
            'components_first': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'components_first'}),
            'canal_b': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'canal'}),
            'canal_p': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'canal'}),
            'work_length_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'work_length'}),
            'work_length_p': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'work_length'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'second_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'components_second': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'components_second'}),
            'third_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'components_third': forms.CheckboxSelectMultiple( attrs={'class': 'form-control', 'placeholder': 'components_third'}),
            'fourth_visit': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'components_fourth': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'components_fourth'}),
            'filling_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'filling_type'}),
            'filling_type1': forms.Select(attrs={'class': 'form-control', 'placeholder': 'filling_type'}),
            'filling_type2': forms.Select(attrs={'class': 'form-control', 'placeholder': 'filling_type'}),
            'filling_type3': forms.Select(attrs={'class': 'form-control', 'placeholder': 'filling_type'}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']


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


class VisitsForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = ['visit_name']
        labels = {
            'visit_name': '',}
        widgets = {
            'visit_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'visit_name'}),}


class OrthoForm(forms.ModelForm):
    exo_images = forms.FileInput()
    visits = forms.ModelChoiceField(queryset=Visits.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), empty_label="Select Visits",
                                    to_field_name='visit_name',
                                    required=False,  # Mark the field as not required
                                    initial=None) # Set the initial value to None
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)

    class Meta:
        model = Ortho
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth', 'ur', 'ul','lr', 'll',  'urn', 'uln','lrn', 'lln','teeth_type', 'angle_class',
                  'over_jet','over_bt', 'jow_shift', 'midlin_shift','urs', 'uls','lrs', 'lls','teeth_size','SNA_before','SNA_after','SNB_before','SNB_after','ANB_before','ANB_after',
                  'IMPA_before','IMPA_after','U1_SN_before','U1_SN_after','SNGOGN_before','SNGOGN_after', 'treatment_plan','price','paid',  'notes','exo_images','visits',
                  'wive_size','cross_sectional','material','brackets','visit_date','uper_date','lower_date','both_date','type_arch','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'urn': '',
            'uln': '',
            'lrn': '',
            'lln': '',
            'teeth_type': '',
            'angle_class': '',
            'over_jet': '',
            'over_bt': '',
            'jow_shift': '',
            'midlin_shift': '',
            'urs': '',
            'uls': '',
            'lrs': '',
            'lls': '',
            'teeth_size': '',
            'SNA_before': '',
            'SNA_after': '',
            'SNB_before': '',
            'SNB_after': '',
            'ANB_before': '',
            'ANB_after': '',
            'IMPA_before': '',
            'IMPA_after': '',
            'U1_SN_before': '',
            'U1_SN_after': '',
            'SNGOGN_before': '',
            'SNGOGN_after': '',
            'treatment_plan': '',
            'price': '',
            'paid': '',
            'notes': '',
            'date': '',
            'visits': '',
            'wive_size': '',
            'cross_sectional': '',
            'material': '',
            'brackets': '',
            'visit_date': '',
            'uper_date': '',
            'lower_date': '',
            'both_date': '',
            'type_arch': '',
            'discount_option': '',
            'price_lab': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'urn': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'urn'}),
            'uln': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'uln'}),
            'lrn': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'urn'}),
            'lln': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lln'}),
            'teeth_type': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'canal'}),
            'angle_class': forms.Select(attrs={'class': 'form-control', 'placeholder': 'angle_class'}),
            'over_jet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'over_jet'}),
            'over_bt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'over_bt'}),
            'jow_shift': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'jow_shift'}),
            'midlin_shift': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'midlin_shift'}),
            'urs': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'uls': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lrs': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'lls': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'teeth_size': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'SNA_before': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'SNA_after': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'SNB_before': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'components_second'}),
            'SNB_after': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'ANB_before': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'components_second'}),
            'ANB_after': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'IMPA_before': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'components_second'}),
            'IMPA_after': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'U1_SN_before': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'components_second'}),
            'U1_SN_after': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'SNGOGN_before': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'components_second'}),
            'SNGOGN_after': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'components_third'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'wive_size': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'cross_sectional': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'material': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'brackets': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'visit_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'uper_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'lower_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'both_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'type_arch': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),

        }


class DebtsForm(forms.ModelForm):
    class Meta:
        model = Debts
        fields = ('idReception', 'idExo', 'idFilling', 'idCrown', 'idVeneer', 'idOralSurgery', 'totalPrice', 'paid', 'remaining')
        labels = {
            'idReception': '',
            'idExo': '',
            'idFilling': '',
            'idCrown': '',
            'idVeneer': '',
            'idOralSurgery': '',
            'totalPrice': '',
            'paid': '',
            'remaining': '',
        }
        widgets = {
            'idReception': forms.TextInput(attrs={'class': 'form-control'}),
            'idExo': forms.TextInput(attrs={'class': 'form-control'}),
            'idFilling': forms.TextInput(attrs={'class': 'form-control'}),
            'idCrown': forms.TextInput(attrs={'class': 'form-control'}),
            'idVeneer': forms.TextInput(attrs={'class': 'form-control'}),
            'idOralSurgery': forms.TextInput(attrs={'class': 'form-control'}),
            'totalPrice': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'totalPrice'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'remaining': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'remaining'}),
        }


class ProsthodonticsForm(forms.ModelForm):
    exo_images = forms.FileInput()
    lab_name = forms.ModelChoiceField(queryset=Lab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label='Select Lab', required=False)
    class Meta:
        model = Prosthodontics
        fields = ('idReception','idReception1', 'idReception', 'name', 'phone', 'gender', 'date_of_birth','ur', 'ul', 'lr', 'll', 'price', 'paid', 'date', 'note','denture', 'upper','lower', 'partial','exo_images','discount_option','lab_name',
                  'price_lab')
        labels = {
            'idReception': '',
            'idReception1': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'denture': '',
            'upper': '',
            'lower': '',
            'partial': '',
            'discount_option': '',
            'lab_name': '',
            'price_lab': '',

        }
        widgets = {
            'idReception': forms.Select(attrs={'class': 'form-control'}),
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'denture': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'denture'}),
            'upper': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'upper'}),
            'lower': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'placeholder': 'complcated'}),
            'partial': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'placeholder': 'complcated'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),

        }


class PaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['idReception','idReception1', 'crown_instance', 'endo_instance', 'filling_instance','pedo_instance', 'oral_surgery_instance', 'ortho_instance', 'veneer_instance', 'periodontology_instance', 'prosthodontics_instance', 'xrays_instance', 'surgery_instance','preventive_instance','exo_instance', 'previous_date', 'paid_amount', 'price', 'name', 'phone']


class StoreForm(forms.ModelForm):
    material_name = forms.ModelChoiceField(queryset=Material.objects.all(),widget=forms.Select(attrs=
                                           {'class': 'form-control'}), empty_label='Select Material', required=True)

    class Meta:
        model = Store
        fields = ('barcode','quantity', 'shelf_Num', 'price', 'expire_date','user','material_name')
        labels = {
            'barcode': '',
            'quantity': '',
            'shelf_Num': '',
            'price': '',
            'gender': '',
            'date_of_birth': '',
            'material_name': '',

        }
        widgets = {
            'material_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'shelf_Num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter shelf number'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'expire_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter expiration date', 'type': 'date'}),
        }

        def clean_Quantity(self):
            quantity = self.cleaned_data.get('Quantity')
            if quantity is None:
                return 0
            return int(quantity)  # Ensure Quantity is returned as an integer


class MaterialOutputForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}) , empty_label="Select Doctor",
                                    to_field_name='doctor_name')
    class Meta:
        model = MaterialOutput
        fields = ['doctor','quantity', 'barcode','material_out','quantity_in']
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity to output'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'material_out': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'quantity_in': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        try:
            quantity = int(quantity)
        except ValueError:
            raise forms.ValidationError('Quantity must be a valid integer.')

        if quantity <= 0:
            raise forms.ValidationError('Quantity must be a positive number.')

        return quantity


class XraysForm(forms.ModelForm):
    exo_images = forms.FileInput()

    class Meta:
        model = Xrays
        fields = ('idReception','idReception1', 'name', 'phone', 'gender', 'date_of_birth','ur', 'ul', 'lr', 'll', 'price',
                  'paid','date', 'note', 'type_xrays')
        labels = {
            'idReception1': '',
            'idExo': '',
            'name': '',
            'phone': '',
            'gender': '',
            'date_of_birth': '',
            'ur': '',
            'ul': '',
            'lr': '',
            'll': '',
            'price': '',
            'paid': '',
            'note': '',
            'date': '',
            'type_xrays': '',



        }
        widgets = {
            'idReception1': forms.Select(attrs={'class': 'form-control'}),
            'idExo': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'gender'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'date_of_birth'}),
            'ur': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ur'}),
            'ul': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'ul'}),
            'lr': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'lr'}),
            'll': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'll'}),

            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'price_lab': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'lab_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'paid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'paid'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'note'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'type_xrays': forms.Select(attrs={'class': 'form-control', 'placeholder': 'type_xrays'}),
        }


MODEL_CHOICES = [
    ('exo', 'Exo'),
    ('implant', 'Implant'),
    ('endo', 'Endo'),
    ('filling', 'Filling'),
    ('veneer', 'Veneer'),
    ('crown', 'Crown'),
    # Add other models here
]


class SearchFormModel(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    model_choice = forms.ChoiceField(choices=MODEL_CHOICES, required=False)  # Add this field