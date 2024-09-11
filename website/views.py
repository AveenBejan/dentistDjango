
from django.shortcuts import render,redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, AppointmentForm,DentistDetailsForm,ReceptionForm,OralSurgeryForm,OrthoForm,ExoForm,\
    MedicinForm,PhotoForm,DrugForm,CrownForm,Medicine1Form,VeneerForm,FillingForm,DrugFormSet,DoctorsForm,SearchForm,\
    ImplantForm,GaveAppointmentForm,DebtsForm,PaymentHistoryForm,BasicInfoForm,SalaryForm,OutcomeForm, EndoForm,VisitsForm,EducationalForm,\
    SearchForm1,PeriodontologyForm,ProsthodonticsForm,UploadFileForm,ReceptionForm1,PedoForm,StoreForm,MaterialForm,LabForm,MaterialOutputForm,XraysForm,SurgeryForm,PreventiveForm,SearchFormModel
from .models import Appointment1,DentistDetails,Reception,OralSurgery,Ortho,Exo,Medicin,\
    Photo,Drug,Medicine1,Crown,Veneer,Filling,Doctors,Implant,GaveAppointment,Debts,BasicInfo,Salary,Outcome,Endo,Visits,Educational,Periodontology,Prosthodontics,\
    UploadedFile,WebsiteFeedback,PaymentHistory,Reception1,Pedo,Store,Material,Lab,MaterialOutput,Xrays,Surgery,Preventive
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date,timedelta
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse

from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from django.http import Http404
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from decimal import Decimal
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.db.models import Sum, F, Q, Value, IntegerField
from django.db.models.functions import Coalesce
from decimal import Decimal, InvalidOperation
import barcode
from barcode.writer import ImageWriter
from django.http import HttpResponse
from io import BytesIO
from .models import GeneratedBarcode
import uuid

def barcode_view(request):
    barcode_instance = None

    if request.method == 'POST':
        barcode_str = request.POST.get('barcode')

        if barcode_str:
            # Create or get the existing barcode instance
            barcode_instance, created = GeneratedBarcode.objects.get_or_create(barcode=barcode_str)

            # If it is newly created, save the barcode image
            if created:
                barcode_instance.save()
        else:
            # Generate a unique barcode string
            barcode_str = generate_unique_barcode()
            # Create a new barcode instance
            barcode_instance, created = GeneratedBarcode.objects.get_or_create(barcode=barcode_str)
            if created:
                barcode_instance.save()

    # If a barcode was found or created, show its details; otherwise, just show the form
    return render(request, 'store/barcode_view.html', {'barcode': barcode_instance})


def generate_unique_barcode():
    # Generate a unique barcode string using UUID
    unique_id = uuid.uuid4().hex[:12].upper()  # Create a unique string with length 12
    return unique_id


def custom_login(request):
    if request.method == 'POST':
        # Your existing login logic
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # Check if the user's role is "patient"
            if user.role == 'patient':
                # Redirect to user_all.html for patients
                return redirect('user_all')
            else:
                # Redirect to another page for users with roles other than "patient"
                return redirect('home')  # Replace 'dashboard' with your desired URL

    # Render the login page for GET requests or failed login attempts
    return render(request, 'login.html')


def feedback_view(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = WebsiteFeedbackForm(request.POST)
            if form.is_valid():
                form.save()  # Save the feedback if the form is valid
                return JsonResponse({'success': True})  # Return JSON response for success
            else:
                return JsonResponse({'success': False})  # Return JSON response for failure
        else:
            form = WebsiteFeedbackForm(request.POST)
            if form.is_valid():
                form.save()  # Save the feedback if the form is valid
                return HttpResponseRedirect('feedback_view')  # Redirect after successful feedback submission

    else:
        form = WebsiteFeedbackForm()

    return render(request, 'home.html', {'form': form})


def upload_file(request):
    uploaded_files = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload')
    else:
        form = UploadFileForm()
        uploaded_files = UploadedFile.objects.all()  # Replace UploadedFile with your model name
    return render(request, 'upload.html', {'form': form,'uploaded_files': uploaded_files})


def delete_upload_file(request,id):
    uploaded_files = UploadedFile.objects.get(pk=id)
    uploaded_files.delete()
    return redirect('upload')


def generate_pdf_view(html_content, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    buffer = BytesIO()

    # Create a PDF object from the HTML content
    pisa.CreatePDF(BytesIO(html_content.encode("UTF-8")), buffer)

    # Write the PDF contents to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def crown_pdf(request, template_name, context):
    # Register the Arabic font for embedding
    pdfmetrics.registerFont(TTFont('arabic', r'E:\projects\dentistsite\dentist\static\website\fonts\Arial.ttf'))

    # Get the HTML content from a template
    html_template = get_template(template_name)

    html_content = html_template.render(context)
    filename = "print_crown_debt.pdf"  # Desired PDF filename

    return generate_pdf_view(html_content, filename)


def add_outcome(request):
    if request.method == 'POST':
        form = OutcomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-outcome')  # Redirect to the same page after saving the form data
    else:
        form = OutcomeForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Outcome.objects.all().order_by('-regdate')
    return render(request, 'outcome/add_outcome.html', {'form': form, 'appointments': appointments})


def delete_outcome(request,id):
    appointments = Outcome.objects.get(pk=id)
    appointments.delete()
    return redirect('add-outcome')


def delete_store(request,id):
    appointments = Store.objects.get(pk=id)
    appointments.delete()
    return redirect('add_store')


def add_new_employ(request):
    if request.method == 'POST':
        form = BasicInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-new-employ')  # Redirect to the same page after saving the form data
    else:
        form = BasicInfoForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = BasicInfo.objects.all().order_by('-regdate')
    return render(request, 'employs/add_new_employ.html', {'form': form, 'appointments': appointments})


def update_employ(request, id):
    basic_info = get_object_or_404(BasicInfo, pk=id)
    form = BasicInfoForm(instance=basic_info)  # Initialize form variable

    if request.method == 'POST':
        form = BasicInfoForm(request.POST, instance=basic_info)
        if form.is_valid():
            form.save()
            return redirect('add-new-employ')  # Redirect to a success page or appropriate URL
        else:
            print(form.errors)  # Check for form errors in the console

    return render(request, 'employs/update_employ.html', {'form': form})


def salary_reception(request):

    appointments = BasicInfo.objects.all().order_by('-regdate')
    return render(request, 'employs/salary_reception.html', {'appointments': appointments})


def delete_employ(request,id):
    appointments = BasicInfo.objects.get(pk=id)
    appointments.delete()
    return redirect('add-new-employ')


def add_salary(request, id):
    try:
        basicinfo = BasicInfo.objects.get(id=id)
    except BasicInfo.DoesNotExist:
        return HttpResponse("BasicInfo with ID does not exist")

    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            # Check if a record for the same month already exists
            month = form.cleaned_data['month']
            existing_record = Salary.objects.filter(idBasicInfo=basicinfo, month=month).exists()

            if existing_record:
                # Display an alert message if a record for the same month exists
                messages.error(request, f"You have already submitted salary for {month}.")
            else:
                salaryPaid = form.cleaned_data['salaryPaid']
                days = form.cleaned_data['days']
                finalSalary = salaryPaid * days

                oral_surgery = form.save(commit=False)
                oral_surgery.idBasicInfo = basicinfo
                oral_surgery.finalSalary = finalSalary
                oral_surgery.fullname = basicinfo.fullname
                oral_surgery.salaryPaid = basicinfo.salaryPaid
                oral_surgery.month = month
                oral_surgery.save()
                return redirect('add-salary', id=id)
    else:
        initial_data = {
            'idBasicInfo': id,
            'fullname': basicinfo.fullname,
            'salaryPaid': basicinfo.salaryPaid,
            'month': date.today().strftime('%B')
        }
        form = SalaryForm(initial=initial_data)

    appointments = Salary.objects.all().order_by('-id')

    return render(request, 'employs/add_salary.html', {'form': form, 'appointments': appointments})


def search_view(request):
    query = request.GET.get('query')  # Get the search query

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()

    if query:
        exos = Exo.objects.filter(name=query)
        fillings = Filling.objects.filter(name=query)
        crowns = Crown.objects.filter(name=query)
        veneers = Veneer.objects.filter(name=query)
        oralSurgery = OralSurgery.objects.filter(name=query)
        endos = Endo.objects.filter(name=query)
        orthos = Ortho.objects.filter(name=query)

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))

    context = {
        'query': query,
        'search_results': search_results,
    }

    return render(request, 'search.html', context)


def search_debts(request):
    query = request.GET.get('query', '').lower()  # Get the value of the 'query' parameter from the GET request
    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    prosthodonticss = Prosthodontics.objects.none()
    periodontologys = Periodontology.objects.none()
    pedos = Pedo.objects.none()
    surgerys = Surgery.objects.none()
    preventives = Preventive.objects.none()
    xrayss = Xrays.objects.none()

    if query:
        exos = Exo.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))

        fillings = Filling.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        crowns = Crown.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        veneers = Veneer.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        oralSurgery = OralSurgery.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        endos = Endo.objects.filter(Q(name=query) | Q(name__istartswith=query),idReception__in=Reception1.objects.values('idReception'))
        orthos = Ortho.objects.filter(Q(name=query) | Q(name__istartswith=query),idReception__in=Reception1.objects.values('idReception'),visits_id__isnull=True)
        prosthodonticss = Prosthodontics.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        periodontologys = Periodontology.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        pedos = Pedo.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        surgerys = Surgery.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        preventives = Preventive.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        xrayss = Xrays.objects.filter(Q(name__istartswith=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))
    if prosthodonticss.exists():
        search_results.append(('Prosthodontics', prosthodonticss))
    if periodontologys.exists():
        search_results.append(('Periodontology', periodontologys))
    if pedos.exists():
        search_results.append(('Pedo', pedos))
    if preventives.exists():
            search_results.append(('Preventive', preventives))
    if surgerys.exists():
            search_results.append(('Surgery', surgerys))
    if xrayss.exists():
            search_results.append(('Xrays', xrayss))
    context = {
        'query': query,
        'search_results': search_results,
    }

    return render(request, 'finance/search_debts.html', context)


def search_debts_history(request):
    query = request.GET.get('query')  # Get the search query
    paymenthistory = PaymentHistory.objects.none()  # Initialize as an empty queryset
    if query:
        paymenthistory = PaymentHistory.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))

    search_results = []

    if paymenthistory.exists():
        search_results.append(('PaymentHistory', paymenthistory))
    context = {
        'query': query,
        'search_results': search_results,
    }

    return render(request, 'debts/search_debts_history.html', context)


def search_debts1(request):
    query = request.GET.get('query')  # Get the search query

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    prosthodonticss = Prosthodontics.objects.none()
    periodontologys = Periodontology.objects.none()

    if query:
        exos = Exo.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        fillings = Filling.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        crowns = Crown.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        veneers = Veneer.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        oralSurgery = OralSurgery.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        endos = Endo.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        orthos = Ortho.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'), visits_id__isnull=True)
        prosthodonticss = Prosthodontics.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))
        periodontologys = Periodontology.objects.filter(Q(name=query) | Q(phone=query),idReception__in=Reception1.objects.values('idReception'))

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))
    if prosthodonticss.exists():
        search_results.append(('Prosthodontics', prosthodonticss))
    if periodontologys.exists():
        search_results.append(('Periodontology', periodontologys))

    context = {
        'query': query,
        'search_results': search_results,
    }

    return render(request, 'finance/search_debts1.html', context)


def search_educational1(request):
    form = SearchForm1()  # Always instantiate the form
    selected_educational = None  # Initialize the variable

    if request.method == 'POST':
        form = SearchForm1(request.POST)
        if form.is_valid():
            selected_educational = form.cleaned_data.get('educational')

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()  # Initialize as an empty queryset

    if selected_educational:
        exos = Exo.objects.filter(educational=selected_educational)
        fillings = Filling.objects.filter(educational=selected_educational)
        crowns = Crown.objects.filter(educational=selected_educational)
        veneers = Veneer.objects.filter(educational=selected_educational)
        oralSurgery = OralSurgery.objects.filter(educational=selected_educational)
        endos = Endo.objects.filter(educational=selected_educational)
        orthos = Ortho.objects.filter(educational=selected_educational, visits_id__isnull=True)

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))

    # Retrieve Ortho objects where visits_id is not null
    orthos_with_visits = Ortho.objects.filter(educational=selected_educational, visits_id__isnull=False)

    # Clean data before rendering (if needed)
    for orall_instance in orthos_with_visits:
        # Perform any necessary data cleaning for each instance
        # For example:
        # orall_instance.some_field = orall_instance.some_field.replace("'", "")
        orall_instance.save()

    context = {
        'selected_educational': selected_educational,
        'search_results': search_results,
        'orthos_with_visits': orthos_with_visits,  # Pass the Ortho instances to the template
        'form': form
    }

    return render(request, 'educational/search_educational.html', context)


def search_education(request):
    # Query all models directly
    exos = Exo.objects.filter(educational_id__isnull=False)
    fillings = Filling.objects.filter(educational_id__isnull=False)
    crowns = Crown.objects.filter(educational_id__isnull=False)
    veneers = Veneer.objects.filter(educational_id__isnull=False)
    oral_surgeries = OralSurgery.objects.filter(educational_id__isnull=False)
    endos = Endo.objects.filter(educational_id__isnull=False)
    orthos = Ortho.objects.filter(educational_id__isnull=False, visits_id__isnull=True)

    # Combine the querysets into a list for easy iteration in the template
    search_results = [
        ('Exo', exos),
        ('Filling', fillings),
        ('Crown', crowns),
        ('Veneer', veneers),
        ('OralSurgery', oral_surgeries),
        ('Endo', endos),
        ('Ortho', orthos),
    ]
    # Retrieve Ortho objects where visits_id is not null
    orthos_with_visits = Ortho.objects.filter(educational_id__isnull=False, visits_id__isnull=False)

    # Clean data before rendering (if needed)
    for orall_instance in orthos_with_visits:
        # Perform any necessary data cleaning for each instance
        # For example:
        # orall_instance.some_field = orall_instance.some_field.replace("'", "")
        orall_instance.save()
    context = {
        'search_results': search_results,
        'orthos_with_visits': orthos_with_visits,
    }

    return render(request, 'educational/search_eduction.html', context)


def all_debts(request):
    form = SearchForm(request.GET or None)  # Instantiate the form

    # Initialize selected_doctor with None
    selected_doctor = None

    if request.method == 'GET':
        if form.is_valid():
            # Use the correct parameter name based on your URL
            selected_doctor = form.cleaned_data['doctor']

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_datetime = None  # Initialize start_datetime variable
    end_datetime = None  # Initialize end_datetime variable

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    pedos = Pedo.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    periodontologys = Periodontology.objects.none()
    prosthodonticss = Prosthodontics.objects.none()
    surgerys = Surgery.objects.none()
    preventives = Preventive.objects.none()
    xrayss = Xrays.objects.none()

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_datetime = end_datetime + timedelta(days=1)

        date_range_filter = Q(regdate__range=(start_datetime, end_datetime))
        doctor_filter = Q(doctor=selected_doctor) if selected_doctor else Q()

        exos = Exo.objects.filter(date_range_filter & doctor_filter)
        fillings = Filling.objects.filter(date_range_filter & doctor_filter)
        pedos = Pedo.objects.filter(date_range_filter & doctor_filter)
        crowns = Crown.objects.filter(date_range_filter & doctor_filter)
        veneers = Veneer.objects.filter(date_range_filter & doctor_filter)
        oralSurgery = OralSurgery.objects.filter(date_range_filter & doctor_filter)
        endos = Endo.objects.filter(date_range_filter & doctor_filter)
        orthos = Ortho.objects.filter(date_range_filter & doctor_filter & Q(visits_id__isnull=True))
        periodontologys = Periodontology.objects.filter(date_range_filter & doctor_filter)
        prosthodonticss = Prosthodontics.objects.filter(date_range_filter & doctor_filter)
        surgerys = Surgery.objects.filter(date_range_filter & doctor_filter)
        preventives = Preventive.objects.filter(date_range_filter & doctor_filter)
        xrayss = Xrays.objects.filter(date_range_filter & doctor_filter)

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if pedos.exists():
        search_results.append(('Pedo', pedos))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))
    if periodontologys.exists():
        search_results.append(('Periodontology', periodontologys))
    if prosthodonticss.exists():
        search_results.append(('Prosthodontics', prosthodonticss))
    if surgerys.exists():
            search_results.append(('Surgery', surgerys))
    if preventives.exists():
            search_results.append(('Preventive', preventives))
    if xrayss.exists():
            search_results.append(('Xrays', xrayss))


    total_exo = exos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_filling = fillings.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_pedo = pedos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_crown = crowns.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_veneer = veneers.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_oralSurgery = oralSurgery.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_endo = endos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_ortho = orthos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_periodontology = periodontologys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_prosthodontics = prosthodonticss.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_surgery = surgerys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_preventive = preventives.aggregate(center_share=Sum('center_share'))['center_share'] or 0

    total_exo1 = exos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_filling1 = fillings.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_pedo1 = pedos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_crown1 = crowns.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_veneer1 = veneers.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_oralSurgery1 = oralSurgery.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_endo1 = endos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_ortho1 = orthos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_periodontology1 = periodontologys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_prosthodontics1 = prosthodonticss.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_surgery1 = surgerys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_preventive1 = preventives.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0

    total_exo2 = exos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_filling2 = fillings.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_pedo2 = pedos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_crown2 = crowns.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_veneer2 = veneers.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_oralSurgery2 = oralSurgery.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_endo2 = endos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_ortho2 = orthos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_periodontology2 = periodontologys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_prosthodontics2 = prosthodonticss.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_surgery2 = surgerys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_preventive2 = preventives.aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_exo3 = exos.aggregate(price=Sum('price'))['price'] or 0
    total_filling3 = fillings.aggregate(price=Sum('price'))['price'] or 0
    total_pedo3 = pedos.aggregate(price=Sum('price'))['price'] or 0
    total_crown3 = crowns.aggregate(price=Sum('price'))['price'] or 0
    total_veneer3 = veneers.aggregate(price=Sum('price'))['price'] or 0
    total_oralSurgery3 = oralSurgery.aggregate(price=Sum('price'))['price'] or 0
    total_endo3 = endos.aggregate(price=Sum('price'))['price'] or 0
    total_ortho3 = orthos.aggregate(price=Sum('price'))['price'] or 0
    total_periodontology3 = periodontologys.aggregate(price=Sum('price'))['price'] or 0
    total_prosthodontics3 = prosthodonticss.aggregate(price=Sum('price'))['price'] or 0
    total_surgery3 = surgerys.aggregate(price=Sum('price'))['price'] or 0
    total_preventive3 = preventives.aggregate(price=Sum('price'))['price'] or 0
    # Calculate total paid for each type
    paid_exo = exos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_filling = fillings.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_pedo = pedos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_crown = crowns.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_veneer = veneers.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_oralSurgery = oralSurgery.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_endo = endos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_ortho = orthos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_periodontology = periodontologys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_prosthodontics = prosthodonticss.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_surgery = surgerys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_preventive = preventives.aggregate(paid=Sum('paid'))['paid'] or 0
    total_price_t = sum(
        [total_exo, total_filling, total_pedo, total_crown, total_veneer, total_oralSurgery, total_endo, total_ortho,
         total_periodontology, total_prosthodontics, total_surgery, total_preventive])
    total_price_t1 = sum(
        [total_exo1, total_filling1, total_pedo1, total_crown1, total_veneer1, total_oralSurgery1, total_endo1,
         total_ortho1, total_periodontology1, total_prosthodontics1, total_surgery1, total_preventive1])
    total_price_t2 = sum(
        [total_exo2, total_filling2, total_pedo2, total_crown2, total_veneer2, total_oralSurgery2, total_endo2,
         total_ortho2, total_periodontology2, total_prosthodontics2, total_surgery2, total_preventive2])
    total_price_t3 = sum(
        [total_exo3, total_filling3, total_pedo3, total_crown3, total_veneer3, total_oralSurgery3, total_endo3,
         total_ortho3, total_periodontology3, total_prosthodontics3, total_surgery3, total_preventive3])
    total_paid_t = sum(
        [paid_exo, paid_filling, paid_pedo, paid_crown, paid_veneer, paid_oralSurgery, paid_endo, paid_ortho,
         paid_periodontology, paid_prosthodontics, paid_surgery, paid_preventive])
    remaining = total_price_t2 - total_paid_t

    context = {
        'form': form,
        'search_results': search_results,
        'total_exo': total_exo,
        'total_filling': total_filling,
        'total_pedo': total_pedo,
        'total_crown': total_crown,
        'total_veneer': total_veneer,
        'total_oralSurgery': total_oralSurgery,
        'total_endo': total_endo,
        'total_ortho': total_ortho,
        'total_periodontology': total_periodontology,
        'total_prosthodontics': total_prosthodontics,
        'total_surgery': total_surgery,
        'total_preventive': total_preventive,
        'total_exo1': total_exo1,
        'total_filling1': total_filling1,
        'total_pedo1': total_pedo1,
        'total_crown1': total_crown1,
        'total_veneer1': total_veneer1,
        'total_oralSurgery1': total_oralSurgery1,
        'total_endo1': total_endo1,
        'total_ortho1': total_ortho1,
        'total_periodontology1': total_periodontology1,
        'total_prosthodontics1': total_prosthodontics1,
        'total_surgery1': total_surgery1,
        'total_preventive1': total_preventive1,
        'total_exo2': total_exo2,
        'total_filling2': total_filling2,
        'total_pedo2': total_pedo2,
        'total_crown2': total_crown2,
        'total_veneer2': total_veneer2,
        'total_oralSurgery2': total_oralSurgery2,
        'total_endo2': total_endo2,
        'total_ortho2': total_ortho2,
        'total_periodontology2': total_periodontology2,
        'total_prosthodontics2': total_prosthodontics2,
        'total_surgery2': total_surgery2,
        'total_preventive2': total_preventive2,
        'total_exo3': total_exo3,
        'total_filling3': total_filling3,
        'total_pedo3': total_pedo3,
        'total_crown3': total_crown3,
        'total_veneer3': total_veneer3,
        'total_oralSurgery3': total_oralSurgery3,
        'total_endo3': total_endo3,
        'total_ortho3': total_ortho3,
        'total_periodontology3': total_periodontology3,
        'total_prosthodontics3': total_prosthodontics3,
        'total_surgery3': total_surgery3,
        'total_preventive3': total_preventive3,
        'paid_exo': paid_exo,
        'paid_filling': paid_filling,
        'paid_pedo': paid_pedo,
        'paid_crown': paid_crown,
        'paid_veneer': paid_veneer,
        'paid_oralSurgery': paid_oralSurgery,
        'paid_endo': paid_endo,
        'paid_ortho': paid_ortho,
        'paid_periodontology': paid_periodontology,
        'paid_prosthodontics': paid_prosthodontics,
        'paid_surgery': paid_surgery,
        'paid_preventive': paid_preventive,
        'total_price_t': total_price_t,
        'total_price_t1': total_price_t1,
        'total_price_t2': total_price_t2,
        'total_price_t3': total_price_t3,
        'total_paid_t': total_paid_t,
        'remaining': remaining,
        'start_date': start_date,  # Add this line
        'end_date': end_date  # Add this line
    }

    return render(request, 'debts/all_debts.html', context)


def all_model(request):
    form = SearchFormModel(request.GET or None)  # Instantiate the form

    selected_model = None
    queryset = None

    # Initialize all variables to empty querysets
    exos = Exo.objects.none()
    fillings = Filling.objects.none()
    pedos = Pedo.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    periodontologys = Periodontology.objects.none()
    prosthodonticss = Prosthodontics.objects.none()
    surgerys = Surgery.objects.none()
    preventives = Preventive.objects.none()

    if request.method == 'GET' and form.is_valid():
        selected_model = form.cleaned_data.get('model_choice')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_datetime = end_datetime + timedelta(days=1)

        date_range_filter = Q(regdate__range=(start_datetime, end_datetime))

        search_results = []

        if selected_model == 'Exo':
            exos = Exo.objects.filter(date_range_filter)
            if exos.exists():
                search_results.append(('Exo', exos))
        elif selected_model == 'Filling':
            fillings = Filling.objects.filter(date_range_filter)
            if fillings.exists():
                search_results.append(('Filling', fillings))
        elif selected_model == 'Pedo':
            pedos = Pedo.objects.filter(date_range_filter)
            if pedos.exists():
                search_results.append(('Pedo', pedos))
        elif selected_model == 'Crown':
            crowns = Crown.objects.filter(date_range_filter)
            if crowns.exists():
                search_results.append(('Crown', crowns))
        elif selected_model == 'Veneer':
            veneers = Veneer.objects.filter(date_range_filter)
            if veneers.exists():
                search_results.append(('Veneer', veneers))
        elif selected_model == 'OralSurgery':
            oralSurgery = OralSurgery.objects.filter(date_range_filter)
            if oralSurgery.exists():
                search_results.append(('OralSurgery', oralSurgery))
        elif selected_model == 'Endo':
            endos = Endo.objects.filter(date_range_filter)
            if endos.exists():
                search_results.append(('Endo', endos))
        elif selected_model == 'Ortho':
            orthos = Ortho.objects.filter(date_range_filter & Q(visits_id__isnull=True))
            if orthos.exists():
                search_results.append(('Ortho', orthos))
        elif selected_model == 'Periodontology':
            periodontologys = Periodontology.objects.filter(date_range_filter)
            if periodontologys.exists():
                search_results.append(('Periodontology', periodontologys))
        elif selected_model == 'Prosthodontics':
            prosthodonticss = Prosthodontics.objects.filter(date_range_filter)
            if prosthodonticss.exists():
                search_results.append(('Prosthodontics', prosthodonticss))
        elif selected_model == 'Surgery':
            surgerys = Surgery.objects.filter(date_range_filter)
            if surgerys.exists():
                search_results.append(('Surgery', surgerys))
        elif selected_model == 'Preventive':
            preventives = Preventive.objects.filter(date_range_filter)
            if preventives.exists():
                search_results.append(('Preventive', preventives))

    else:
        search_results = []

    # Calculate totals
    total_exo = exos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_filling = fillings.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_pedo = pedos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_crown = crowns.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_veneer = veneers.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_oralSurgery = oralSurgery.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_endo = endos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_ortho = orthos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_periodontology = periodontologys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_prosthodontics = prosthodonticss.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_surgery = surgerys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_preventive = preventives.aggregate(center_share=Sum('center_share'))['center_share'] or 0

    total_exo1 = exos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_filling1 = fillings.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_pedo1 = pedos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_crown1 = crowns.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_veneer1 = veneers.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_oralSurgery1 = oralSurgery.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_endo1 = endos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_ortho1 = orthos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_periodontology1 = periodontologys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_prosthodontics1 = prosthodonticss.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_surgery1 = surgerys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_preventive1 = preventives.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0

    total_exo2 = exos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_filling2 = fillings.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_pedo2 = pedos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_crown2 = crowns.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_veneer2 = veneers.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_oralSurgery2 = oralSurgery.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_endo2 = endos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_ortho2 = orthos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_periodontology2 = periodontologys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_prosthodontics2 = prosthodonticss.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_surgery2 = surgerys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_preventive2 = preventives.aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_exo3 = exos.aggregate(price=Sum('price'))['price'] or 0
    total_filling3 = fillings.aggregate(price=Sum('price'))['price'] or 0
    total_pedo3 = pedos.aggregate(price=Sum('price'))['price'] or 0
    total_crown3 = crowns.aggregate(price=Sum('price'))['price'] or 0
    total_veneer3 = veneers.aggregate(price=Sum('price'))['price'] or 0
    total_oralSurgery3 = oralSurgery.aggregate(price=Sum('price'))['price'] or 0
    total_endo3 = endos.aggregate(price=Sum('price'))['price'] or 0
    total_ortho3 = orthos.aggregate(price=Sum('price'))['price'] or 0
    total_periodontology3 = periodontologys.aggregate(price=Sum('price'))['price'] or 0
    total_prosthodontics3 = prosthodonticss.aggregate(price=Sum('price'))['price'] or 0
    total_surgery3 = surgerys.aggregate(price=Sum('price'))['price'] or 0
    total_preventive3 = preventives.aggregate(price=Sum('price'))['price'] or 0
    # Calculate total paid for each type
    paid_exo = exos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_filling = fillings.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_pedo = pedos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_crown = crowns.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_veneer = veneers.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_oralSurgery = oralSurgery.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_endo = endos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_ortho = orthos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_periodontology = periodontologys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_prosthodontics = prosthodonticss.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_surgery = surgerys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_preventive = preventives.aggregate(paid=Sum('paid'))['paid'] or 0
    total_price_t = sum(
        [total_exo, total_filling, total_pedo, total_crown, total_veneer, total_oralSurgery, total_endo, total_ortho,
         total_periodontology, total_prosthodontics, total_surgery, total_preventive])
    total_price_t1 = sum(
        [total_exo1, total_filling1, total_pedo1, total_crown1, total_veneer1, total_oralSurgery1, total_endo1,
         total_ortho1, total_periodontology1, total_prosthodontics1, total_surgery1, total_preventive1])
    total_price_t2 = sum(
        [total_exo2, total_filling2, total_pedo2, total_crown2, total_veneer2, total_oralSurgery2, total_endo2,
         total_ortho2, total_periodontology2, total_prosthodontics2, total_surgery2, total_preventive2])
    total_price_t3 = sum(
        [total_exo3, total_filling3, total_pedo3, total_crown3, total_veneer3, total_oralSurgery3, total_endo3,
         total_ortho3, total_periodontology3, total_prosthodontics3, total_surgery3, total_preventive3])
    total_paid_t = sum(
        [paid_exo, paid_filling, paid_pedo, paid_crown, paid_veneer, paid_oralSurgery, paid_endo, paid_ortho,
         paid_periodontology, paid_prosthodontics, paid_surgery, paid_preventive])
    remaining = total_price_t2 - total_paid_t

    context = {
        'form': form,
        'search_results': search_results,
        'total_exo': total_exo,
        'total_filling': total_filling,
        'total_pedo': total_pedo,
        'total_crown': total_crown,
        'total_veneer': total_veneer,
        'total_oralSurgery': total_oralSurgery,
        'total_endo': total_endo,
        'total_ortho': total_ortho,
        'total_periodontology': total_periodontology,
        'total_prosthodontics': total_prosthodontics,
        'total_surgery': total_surgery,
        'total_preventive': total_preventive,
        'total_exo1': total_exo1,
        'total_filling1': total_filling1,
        'total_pedo1': total_pedo1,
        'total_crown1': total_crown1,
        'total_veneer1': total_veneer1,
        'total_oralSurgery1': total_oralSurgery1,
        'total_endo1': total_endo1,
        'total_ortho1': total_ortho1,
        'total_periodontology1': total_periodontology1,
        'total_prosthodontics1': total_prosthodontics1,
        'total_surgery1': total_surgery1,
        'total_preventive1': total_preventive1,
        'total_exo2': total_exo2,
        'total_filling2': total_filling2,
        'total_pedo2': total_pedo2,
        'total_crown2': total_crown2,
        'total_veneer2': total_veneer2,
        'total_oralSurgery2': total_oralSurgery2,
        'total_endo2': total_endo2,
        'total_ortho2': total_ortho2,
        'total_periodontology2': total_periodontology2,
        'total_prosthodontics2': total_prosthodontics2,
        'total_surgery2': total_surgery2,
        'total_preventive2': total_preventive2,
        'total_exo3': total_exo3,
        'total_filling3': total_filling3,
        'total_pedo3': total_pedo3,
        'total_crown3': total_crown3,
        'total_veneer3': total_veneer3,
        'total_oralSurgery3': total_oralSurgery3,
        'total_endo3': total_endo3,
        'total_ortho3': total_ortho3,
        'total_periodontology3': total_periodontology3,
        'total_prosthodontics3': total_prosthodontics3,
        'total_surgery3': total_surgery3,
        'total_preventive3': total_preventive3,
        'paid_exo': paid_exo,
        'paid_filling': paid_filling,
        'paid_pedo': paid_pedo,
        'paid_crown': paid_crown,
        'paid_veneer': paid_veneer,
        'paid_oralSurgery': paid_oralSurgery,
        'paid_endo': paid_endo,
        'paid_ortho': paid_ortho,
        'paid_periodontology': paid_periodontology,
        'paid_prosthodontics': paid_prosthodontics,
        'paid_surgery': paid_surgery,
        'paid_preventive': paid_preventive,
        'total_price_t': total_price_t,
        'total_price_t1': total_price_t1,
        'total_price_t2': total_price_t2,
        'total_price_t3': total_price_t3,
        'total_paid_t': total_paid_t,
        'remaining': remaining,
        'start_date': start_date,  # Add this line
        'end_date': end_date  # Add this line
    }

    return render(request, 'debts/all_model.html', context)


def earnings(request):
    form = SearchForm(request.GET or None)  # Instantiate the form

    # Initialize selected_doctor with None
    selected_doctor = None

    if request.method == 'GET':
        if form.is_valid():
            # Use the correct parameter name based on your URL
            selected_doctor = form.cleaned_data['doctor']

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_datetime = None  # Initialize start_datetime variable
    end_datetime = None  # Initialize end_datetime variable

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    pedos = Pedo.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    periodontologys = Periodontology.objects.none()
    prosthodonticss = Prosthodontics.objects.none()
    surgerys = Surgery.objects.none()
    preventives = Preventive.objects.none()

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_datetime = end_datetime + timedelta(days=1)

        date_range_filter = Q(regdate__range=(start_datetime, end_datetime))
        doctor_filter = Q(doctor=selected_doctor) if selected_doctor else Q()

        exos = Exo.objects.filter(date_range_filter & doctor_filter)
        fillings = Filling.objects.filter(date_range_filter & doctor_filter)
        pedos = Pedo.objects.filter(date_range_filter & doctor_filter)
        crowns = Crown.objects.filter(date_range_filter & doctor_filter)
        veneers = Veneer.objects.filter(date_range_filter & doctor_filter)
        oralSurgery = OralSurgery.objects.filter(date_range_filter & doctor_filter)
        endos = Endo.objects.filter(date_range_filter & doctor_filter)
        orthos = Ortho.objects.filter(date_range_filter & doctor_filter & Q(visits_id__isnull=True))
        periodontologys = Periodontology.objects.filter(date_range_filter & doctor_filter)
        prosthodonticss = Prosthodontics.objects.filter(date_range_filter & doctor_filter)
        surgerys = Surgery.objects.filter(date_range_filter & doctor_filter)
        preventives = Preventive.objects.filter(date_range_filter & doctor_filter)

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if pedos.exists():
        search_results.append(('Pedo', pedos))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))
    if periodontologys.exists():
        search_results.append(('Periodontology', periodontologys))
    if prosthodonticss.exists():
        search_results.append(('Prosthodontics', prosthodonticss))
    if surgerys.exists():
        search_results.append(('Surgery', surgerys))
    if preventives.exists():
        search_results.append(('Preventive', preventives))

    total_exo = exos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_filling = fillings.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_pedo = pedos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_crown = crowns.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_veneer = veneers.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_oralSurgery = oralSurgery.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_endo = endos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_ortho = orthos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_periodontology = periodontologys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_prosthodontics = prosthodonticss.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_surgery = surgerys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_preventive = preventives.aggregate(center_share=Sum('center_share'))['center_share'] or 0

    total_exo1 = exos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_filling1 = fillings.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_pedo1 = pedos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_crown1 = crowns.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_veneer1 = veneers.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_oralSurgery1 = oralSurgery.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_endo1 = endos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_ortho1 = orthos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_periodontology1 = periodontologys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_prosthodontics1 = prosthodonticss.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_surgery1 = surgerys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_preventive1 = preventives.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0

    total_exo2 = exos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_filling2 = fillings.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_pedo2 = pedos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_crown2 = crowns.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_veneer2 = veneers.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_oralSurgery2 = oralSurgery.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_endo2 = endos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_ortho2 = orthos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_periodontology2 = periodontologys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_prosthodontics2 = prosthodonticss.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_surgery2 = surgerys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_preventive2 = preventives.aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_exo3 = exos.aggregate(price=Sum('price'))['price'] or 0
    total_filling3 = fillings.aggregate(price=Sum('price'))['price'] or 0
    total_pedo3 = pedos.aggregate(price=Sum('price'))['price'] or 0
    total_crown3 = crowns.aggregate(price=Sum('price'))['price'] or 0
    total_veneer3 = veneers.aggregate(price=Sum('price'))['price'] or 0
    total_oralSurgery3 = oralSurgery.aggregate(price=Sum('price'))['price'] or 0
    total_endo3 = endos.aggregate(price=Sum('price'))['price'] or 0
    total_ortho3 = orthos.aggregate(price=Sum('price'))['price'] or 0
    total_periodontology3 = periodontologys.aggregate(price=Sum('price'))['price'] or 0
    total_prosthodontics3 = prosthodonticss.aggregate(price=Sum('price'))['price'] or 0
    total_surgery3 = surgerys.aggregate(price=Sum('price'))['price'] or 0
    total_preventive3 = preventives.aggregate(price=Sum('price'))['price'] or 0
    # Calculate total paid for each type
    paid_exo = exos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_filling = fillings.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_pedo = pedos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_crown = crowns.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_veneer = veneers.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_oralSurgery = oralSurgery.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_endo = endos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_ortho = orthos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_periodontology = periodontologys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_prosthodontics = prosthodonticss.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_surgery = surgerys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_preventive = preventives.aggregate(paid=Sum('paid'))['paid'] or 0
    total_price_t = sum(
        [total_exo, total_filling, total_pedo, total_crown, total_veneer, total_oralSurgery, total_endo, total_ortho,
         total_periodontology, total_prosthodontics, total_surgery, total_preventive])
    total_price_t1 = sum(
        [total_exo1, total_filling1, total_pedo1, total_crown1, total_veneer1, total_oralSurgery1, total_endo1,
         total_ortho1, total_periodontology1, total_prosthodontics1, total_surgery1, total_preventive1])
    total_price_t2 = sum(
        [total_exo2, total_filling2, total_pedo2, total_crown2, total_veneer2, total_oralSurgery2, total_endo2,
         total_ortho2, total_periodontology2, total_prosthodontics2, total_surgery2, total_preventive2])
    total_price_t3 = sum(
        [total_exo3, total_filling3, total_pedo3, total_crown3, total_veneer3, total_oralSurgery3, total_endo3,
         total_ortho3, total_periodontology3, total_prosthodontics3, total_surgery3, total_preventive3])
    total_paid_t = sum(
        [paid_exo, paid_filling, paid_pedo, paid_crown, paid_veneer, paid_oralSurgery, paid_endo, paid_ortho,
         paid_periodontology, paid_prosthodontics, paid_surgery, paid_preventive])
    remaining = total_price_t2 - total_paid_t

    context = {
        'form': form,
        'search_results': search_results,
        'total_exo': total_exo,
        'total_filling': total_filling,
        'total_pedo': total_pedo,
        'total_crown': total_crown,
        'total_veneer': total_veneer,
        'total_oralSurgery': total_oralSurgery,
        'total_endo': total_endo,
        'total_ortho': total_ortho,
        'total_periodontology': total_periodontology,
        'total_prosthodontics': total_prosthodontics,
        'total_surgery': total_surgery,
        'total_preventive': total_preventive,
        'total_exo1': total_exo1,
        'total_filling1': total_filling1,
        'total_pedo1': total_pedo1,
        'total_crown1': total_crown1,
        'total_veneer1': total_veneer1,
        'total_oralSurgery1': total_oralSurgery1,
        'total_endo1': total_endo1,
        'total_ortho1': total_ortho1,
        'total_periodontology1': total_periodontology1,
        'total_prosthodontics1': total_prosthodontics1,
        'total_surgery1': total_surgery1,
        'total_preventive1': total_preventive1,
        'total_exo2': total_exo2,
        'total_filling2': total_filling2,
        'total_pedo2': total_pedo2,
        'total_crown2': total_crown2,
        'total_veneer2': total_veneer2,
        'total_oralSurgery2': total_oralSurgery2,
        'total_endo2': total_endo2,
        'total_ortho2': total_ortho2,
        'total_periodontology2': total_periodontology2,
        'total_prosthodontics2': total_prosthodontics2,
        'total_surgery2': total_surgery2,
        'total_preventive2': total_preventive2,
        'total_exo3': total_exo3,
        'total_filling3': total_filling3,
        'total_pedo3': total_pedo3,
        'total_crown3': total_crown3,
        'total_veneer3': total_veneer3,
        'total_oralSurgery3': total_oralSurgery3,
        'total_endo3': total_endo3,
        'total_ortho3': total_ortho3,
        'total_periodontology3': total_periodontology3,
        'total_prosthodontics3': total_prosthodontics3,
        'total_surgery3': total_surgery3,
        'total_preventive3': total_preventive3,
        'paid_exo': paid_exo,
        'paid_filling': paid_filling,
        'paid_pedo': paid_pedo,
        'paid_crown': paid_crown,
        'paid_veneer': paid_veneer,
        'paid_oralSurgery': paid_oralSurgery,
        'paid_endo': paid_endo,
        'paid_ortho': paid_ortho,
        'paid_periodontology': paid_periodontology,
        'paid_prosthodontics': paid_prosthodontics,
        'paid_surgery': paid_surgery,
        'paid_preventive': paid_preventive,
        'total_price_t': total_price_t,
        'total_price_t1': total_price_t1,
        'total_price_t2': total_price_t2,
        'total_price_t3': total_price_t3,
        'total_paid_t': total_paid_t,
        'remaining': remaining,
        'start_date': start_date,  # Add this line
        'end_date': end_date  # Add this line
    }
    return render(request, 'debts/earnings.html', context)


def earnings_print(request):
    form = SearchForm(request.GET or None)  # Instantiate the form

    # Initialize selected_doctor with None
    selected_doctor = None

    if request.method == 'GET':
        if form.is_valid():
            # Use the correct parameter name based on your URL
            selected_doctor = form.cleaned_data['doctor']

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_datetime = None  # Initialize start_datetime variable
    end_datetime = None  # Initialize end_datetime variable

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    pedos = Pedo.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    periodontologys = Periodontology.objects.none()
    prosthodonticss = Prosthodontics.objects.none()
    surgerys = Surgery.objects.none()
    preventives = Preventive.objects.none()

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_datetime = end_datetime + timedelta(days=1)

        date_range_filter = Q(regdate__range=(start_datetime, end_datetime))
        doctor_filter = Q(doctor=selected_doctor) if selected_doctor else Q()

        exos = Exo.objects.filter(date_range_filter & doctor_filter)
        fillings = Filling.objects.filter(date_range_filter & doctor_filter)
        pedos = Pedo.objects.filter(date_range_filter & doctor_filter)
        crowns = Crown.objects.filter(date_range_filter & doctor_filter)
        veneers = Veneer.objects.filter(date_range_filter & doctor_filter)
        oralSurgery = OralSurgery.objects.filter(date_range_filter & doctor_filter)
        endos = Endo.objects.filter(date_range_filter & doctor_filter)
        orthos = Ortho.objects.filter(date_range_filter & doctor_filter & Q(visits_id__isnull=True))
        periodontologys = Periodontology.objects.filter(date_range_filter & doctor_filter)
        prosthodonticss = Prosthodontics.objects.filter(date_range_filter & doctor_filter)
        surgerys = Surgery.objects.filter(date_range_filter & doctor_filter)
        preventives = Preventive.objects.filter(date_range_filter & doctor_filter)

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if pedos.exists():
        search_results.append(('Pedo', pedos))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))
    if periodontologys.exists():
        search_results.append(('Periodontology', periodontologys))
    if prosthodonticss.exists():
        search_results.append(('Prosthodontics', prosthodonticss))
    if surgerys.exists():
        search_results.append(('Surgery', surgerys))
    if preventives.exists():
        search_results.append(('Preventive', preventives))

    total_exo = exos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_filling = fillings.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_pedo = pedos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_crown = crowns.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_veneer = veneers.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_oralSurgery = oralSurgery.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_endo = endos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_ortho = orthos.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_periodontology = periodontologys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_prosthodontics = prosthodonticss.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_surgery = surgerys.aggregate(center_share=Sum('center_share'))['center_share'] or 0
    total_preventive = preventives.aggregate(center_share=Sum('center_share'))['center_share'] or 0

    total_exo1 = exos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_filling1 = fillings.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_pedo1 = pedos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_crown1 = crowns.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_veneer1 = veneers.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_oralSurgery1 = oralSurgery.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_endo1 = endos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_ortho1 = orthos.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_periodontology1 = periodontologys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_prosthodontics1 = prosthodonticss.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_surgery1 = surgerys.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0
    total_preventive1 = preventives.aggregate(doctor_share=Sum('doctor_share'))['doctor_share'] or 0

    total_exo2 = exos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_filling2 = fillings.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_pedo2 = pedos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_crown2 = crowns.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_veneer2 = veneers.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_oralSurgery2 = oralSurgery.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_endo2 = endos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_ortho2 = orthos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_periodontology2 = periodontologys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_prosthodontics2 = prosthodonticss.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_surgery2 = surgerys.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_preventive2 = preventives.aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_exo3 = exos.aggregate(price=Sum('price'))['price'] or 0
    total_filling3 = fillings.aggregate(price=Sum('price'))['price'] or 0
    total_pedo3 = pedos.aggregate(price=Sum('price'))['price'] or 0
    total_crown3 = crowns.aggregate(price=Sum('price'))['price'] or 0
    total_veneer3 = veneers.aggregate(price=Sum('price'))['price'] or 0
    total_oralSurgery3 = oralSurgery.aggregate(price=Sum('price'))['price'] or 0
    total_endo3 = endos.aggregate(price=Sum('price'))['price'] or 0
    total_ortho3 = orthos.aggregate(price=Sum('price'))['price'] or 0
    total_periodontology3 = periodontologys.aggregate(price=Sum('price'))['price'] or 0
    total_prosthodontics3 = prosthodonticss.aggregate(price=Sum('price'))['price'] or 0
    total_surgery3 = surgerys.aggregate(price=Sum('price'))['price'] or 0
    total_preventive3 = preventives.aggregate(price=Sum('price'))['price'] or 0
    # Calculate total paid for each type
    paid_exo = exos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_filling = fillings.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_pedo = pedos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_crown = crowns.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_veneer = veneers.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_oralSurgery = oralSurgery.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_endo = endos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_ortho = orthos.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_periodontology = periodontologys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_prosthodontics = prosthodonticss.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_surgery = surgerys.aggregate(paid=Sum('paid'))['paid'] or 0
    paid_preventive = preventives.aggregate(paid=Sum('paid'))['paid'] or 0
    total_price_t = sum(
        [total_exo, total_filling, total_pedo, total_crown, total_veneer, total_oralSurgery, total_endo, total_ortho,
         total_periodontology, total_prosthodontics, total_surgery, total_preventive])
    total_price_t1 = sum(
        [total_exo1, total_filling1, total_pedo1, total_crown1, total_veneer1, total_oralSurgery1, total_endo1,
         total_ortho1, total_periodontology1, total_prosthodontics1, total_surgery1, total_preventive1])
    total_price_t2 = sum(
        [total_exo2, total_filling2, total_pedo2, total_crown2, total_veneer2, total_oralSurgery2, total_endo2,
         total_ortho2, total_periodontology2, total_prosthodontics2, total_surgery2, total_preventive2])
    total_price_t3 = sum(
        [total_exo3, total_filling3, total_pedo3, total_crown3, total_veneer3, total_oralSurgery3, total_endo3,
         total_ortho3, total_periodontology3, total_prosthodontics3, total_surgery3, total_preventive3])
    total_paid_t = sum(
        [paid_exo, paid_filling, paid_pedo, paid_crown, paid_veneer, paid_oralSurgery, paid_endo, paid_ortho,
         paid_periodontology, paid_prosthodontics, paid_surgery, paid_preventive])
    remaining = total_price_t2 - total_paid_t

    context = {
        'form': form,
        'search_results': search_results,
        'total_exo': total_exo,
        'total_filling': total_filling,
        'total_pedo': total_pedo,
        'total_crown': total_crown,
        'total_veneer': total_veneer,
        'total_oralSurgery': total_oralSurgery,
        'total_endo': total_endo,
        'total_ortho': total_ortho,
        'total_periodontology': total_periodontology,
        'total_prosthodontics': total_prosthodontics,
        'total_surgery': total_surgery,
        'total_preventive': total_preventive,
        'total_exo1': total_exo1,
        'total_filling1': total_filling1,
        'total_pedo1': total_pedo1,
        'total_crown1': total_crown1,
        'total_veneer1': total_veneer1,
        'total_oralSurgery1': total_oralSurgery1,
        'total_endo1': total_endo1,
        'total_ortho1': total_ortho1,
        'total_periodontology1': total_periodontology1,
        'total_prosthodontics1': total_prosthodontics1,
        'total_surgery1': total_surgery1,
        'total_preventive1': total_preventive1,
        'total_exo2': total_exo2,
        'total_filling2': total_filling2,
        'total_pedo2': total_pedo2,
        'total_crown2': total_crown2,
        'total_veneer2': total_veneer2,
        'total_oralSurgery2': total_oralSurgery2,
        'total_endo2': total_endo2,
        'total_ortho2': total_ortho2,
        'total_periodontology2': total_periodontology2,
        'total_prosthodontics2': total_prosthodontics2,
        'total_surgery2': total_surgery2,
        'total_preventive2': total_preventive2,
        'total_exo3': total_exo3,
        'total_filling3': total_filling3,
        'total_pedo3': total_pedo3,
        'total_crown3': total_crown3,
        'total_veneer3': total_veneer3,
        'total_oralSurgery3': total_oralSurgery3,
        'total_endo3': total_endo3,
        'total_ortho3': total_ortho3,
        'total_periodontology3': total_periodontology3,
        'total_prosthodontics3': total_prosthodontics3,
        'total_surgery3': total_surgery3,
        'total_preventive3': total_preventive3,
        'paid_exo': paid_exo,
        'paid_filling': paid_filling,
        'paid_pedo': paid_pedo,
        'paid_crown': paid_crown,
        'paid_veneer': paid_veneer,
        'paid_oralSurgery': paid_oralSurgery,
        'paid_endo': paid_endo,
        'paid_ortho': paid_ortho,
        'paid_periodontology': paid_periodontology,
        'paid_prosthodontics': paid_prosthodontics,
        'paid_surgery': paid_surgery,
        'paid_preventive': paid_preventive,
        'total_price_t': total_price_t,
        'total_price_t1': total_price_t1,
        'total_price_t2': total_price_t2,
        'total_price_t3': total_price_t3,
        'total_paid_t': total_paid_t,
        'remaining': remaining,
        'start_date': start_date,  # Add this line
        'end_date': end_date  # Add this line
    }
    return render(request, 'debts/earnings_print.html', context)


def all_debts1(request):
    form = SearchForm(request.GET or None)  # Instantiate the form

    # Initialize selected_doctor with None
    selected_doctor = None

    if request.method == 'GET':
        if form.is_valid():
            # Use the correct parameter name based on your URL
            selected_doctor = form.cleaned_data['doctor']

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    periodontologys = Periodontology.objects.none()
    prosthodonticss = Prosthodontics.objects.none()

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_datetime = end_datetime + timedelta(days=1)

        # Apply doctor filter only if selected_doctor has a value
        if selected_doctor is not None:
            exos = Exo.objects.filter(Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
            fillings = Filling.objects.filter(
                Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
            crowns = Crown.objects.filter(Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
            veneers = Veneer.objects.filter(
                Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
            oralSurgery = OralSurgery.objects.filter(
                Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
            endos = Endo.objects.filter(Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
            orthos = Ortho.objects.filter(Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor) & Q(visits_id__isnull=True))
            periodontologys = Periodontology.objects.filter(Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
            prosthodonticss = Prosthodontics.objects.filter(Q(regdate__range=(start_datetime, end_datetime)) & Q(doctor=selected_doctor))
        else:
            # No matter if selected_doctor is None, perform the query without doctor filter
            exos = Exo.objects.filter(regdate__range=(start_datetime, end_datetime))
            fillings = Filling.objects.filter(regdate__range=(start_datetime, end_datetime))
            crowns = Crown.objects.filter(regdate__range=(start_datetime, end_datetime))
            veneers = Veneer.objects.filter(regdate__range=(start_datetime, end_datetime))
            oralSurgery = OralSurgery.objects.filter(regdate__range=(start_datetime, end_datetime))
            endos = Endo.objects.filter(regdate__range=(start_datetime, end_datetime))
            orthos = Ortho.objects.filter(regdate__range=(start_datetime, end_datetime), visits_id__isnull=True)
            periodontologys = Periodontology.objects.filter(regdate__range=(start_datetime, end_datetime))
            prosthodonticss = Prosthodontics.objects.filter(regdate__range=(start_datetime, end_datetime))

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))
    if periodontologys.exists():
        search_results.append(('Periodontology', periodontologys))
    if prosthodonticss.exists():
        search_results.append(('Prosthodontics', prosthodonticss))


    context = {
        'start_date': start_date,
        'end_date': end_date,
        'selected_doctor': selected_doctor,
        'search_results': search_results,
        'form': form,  # Pass the form to the template for display
    }

    return render(request, 'debts/all_debts1.html', context)


def all_total(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_datetime = None  # Initialize start_datetime variable
    end_datetime = None  # Initialize end_datetime variable

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    pedos = Pedo.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    endos = Endo.objects.none()
    orthos = Ortho.objects.none()
    outcomes = Outcome.objects.none()
    salaries = Salary.objects.none()
    periodontologys = Periodontology.objects.none()
    prosthodonticss = Prosthodontics.objects.none()

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_datetime = end_datetime + timedelta(days=1)

        exos = Exo.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        fillings = Filling.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        pedos = Pedo.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        crowns = Crown.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        veneers = Veneer.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        oralSurgery = OralSurgery.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        endos = Endo.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        orthos = Ortho.objects.filter(Q(regdate__range=(start_datetime, end_datetime)), visits_id__isnull=True)
        periodontologys = Periodontology.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        prosthodonticss = Prosthodontics.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        outcomes = Outcome.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))
        salaries = Salary.objects.filter(Q(regdate__range=(start_datetime, end_datetime)))

    search_results = []

    if exos.exists():
        search_results.append(('Exo', exos))
    if fillings.exists():
        search_results.append(('Filling', fillings))
    if pedos.exists():
        search_results.append(('Pedo', pedos))
    if crowns.exists():
        search_results.append(('Crown', crowns))
    if veneers.exists():
        search_results.append(('Veneer', veneers))
    if oralSurgery.exists():
        search_results.append(('OralSurgery', oralSurgery))
    if endos.exists():
        search_results.append(('Endo', endos))
    if orthos.exists():
        search_results.append(('Ortho', orthos))
    if periodontologys.exists():
        search_results.append(('Periodontology', orthos))
    if prosthodonticss.exists():
        search_results.append(('Prosthodontics', orthos))
    if outcomes.exists():
        search_results.append(('Outcome', outcomes))
    if salaries.exists():
        search_results.append(('Salary', salaries))
    total_exo = Exo.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_filling = Filling.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_pedo = Pedo.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_crown = Crown.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_veneer = Veneer.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_oralSurgery = OralSurgery.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_endo = Endo.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_ortho = Ortho.objects.filter(regdate__range=(start_datetime, end_datetime)).filter(visits_id__isnull=True).aggregate(price_sum=Sum('price'))['price_sum'] or 0
    total_periodontology = Periodontology.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_prosthodontics = Prosthodontics.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_salary = salaries.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_final_salary=Sum('finalSalary'))['total_final_salary'] or 0
    total_outcome = Outcome.objects.filter(regdate__range=(start_datetime, end_datetime)).aggregate(total_price=Sum('price'))['total_price'] or 0
    remaining = ((total_exo+total_filling+total_crown+total_veneer+total_oralSurgery)-(total_salary+total_outcome))

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'search_results': search_results,
        'total_exo': total_exo,  # Add total_salary to the context
        'total_filling': total_filling,  # Add total_salary to the context
        'total_pedo': total_pedo,  # Add total_salary to the context
        'total_crown': total_crown,  # Add total_salary to the context
        'total_veneer': total_veneer,  # Add total_salary to the context
        'total_oralSurgery': total_oralSurgery,  # Add total_salary to the context
        'total_endo': total_endo,  # Add total_salary to the context
        'total_ortho': total_ortho,  # Add total_salary to the context
        'total_periodontology': total_periodontology,  # Add total_salary to the context
        'total_prosthodontics': total_prosthodontics,  # Add total_salary to the context
        'total_salary': total_salary,  # Add total_salary to the context
        'total_outcome': total_outcome,  # Add total_salary to the context
        'remaining': remaining,  # Add total_salary to the context
    }

    return render(request, 'all_total.html', context)


def doctor(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('signup')  # Redirect to the signup page if user doesn't exist

    if request.method == 'POST':
        form = DoctorsForm(request.POST)
        if form.is_valid():
            doctor_instance = form.save(commit=False)  # Create an instance but don't save yet
            doctor_instance.user = user  # Associate the user with the new doctor instance

            proportion_doctor_input = form.cleaned_data.get('proportion_doctor')
            if proportion_doctor_input is not None:
                proportion_doctor = proportion_doctor_input
                proportion_center = 100 - proportion_doctor
            else:
                proportion_doctor = 0
                proportion_center = 0

            salary_input = form.cleaned_data.get('salary')
            salary = salary_input if salary_input is not None else 0

            # Set the calculated proportions and salary
            doctor_instance.proportion_doctor = proportion_doctor
            doctor_instance.proportion_center = proportion_center
            doctor_instance.salary = salary

            # Save the instance
            doctor_instance.save()

        return redirect('doctor', user_id=user_id)   # Redirect to the list of doctors or any other appropriate page
    else:
        form = DoctorsForm()

    # Retrieve all Doctor objects (appointments) from the database and order them by their IDs in ascending order.
    appointments = Doctors.objects.all().order_by('id')
    return render(request, 'doctors/doctor.html', {'form': form, 'appointments': appointments, 'user': user})


def delete_doctor(request, id):
    doctor = get_object_or_404(Doctors, pk=id)
    doctor.delete()
    return redirect('doctor', user_id=request.user.id)


def educational(request):
    if request.method == 'POST':
        form = EducationalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('educational')  # Redirect to the same page after saving the form data
    else:
        form = EducationalForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Educational.objects.all().order_by('-id')
    return render(request, 'educational/educational.html', {'form': form, 'appointments': appointments})


def delete_educational(request,id):
    appointments = Educational.objects.get(pk=id)
    appointments.delete()
    return redirect('educational')


def medicine1(request):
    if request.method == 'POST':
        form = Medicine1Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine1')  # Redirect to the same page after saving the form data
    else:
        form = Medicine1Form()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Medicine1.objects.all().order_by('-id')
    return render(request, 'drugs/medicine1.html', {'form': form, 'appointments': appointments})


def material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material')  # Redirect to the same page after saving the form data
    else:
        form = MaterialForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Material.objects.all().order_by('-id')
    return render(request, 'store/material.html', {'form': form, 'appointments': appointments})


def lab(request):
    if request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab')  # Redirect to the same page after saving the form data
    else:
        form = LabForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Lab.objects.all().order_by('-id')
    return render(request, 'store/lab.html', {'form': form, 'appointments': appointments})


def delete_medicine1(request,id):
    appointments = Medicine1.objects.get(pk=id)
    appointments.delete()
    return redirect('medicine1')


def implant(request):
    if request.method == 'POST':
        form = ImplantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('implant')  # Redirect to the same page after saving the form data
    else:
        form = ImplantForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Implant.objects.all().order_by('-id')
    return render(request, 'implant.html', {'form': form, 'appointments': appointments})


def delete_implant(request,id):
    appointments =  Implant.objects.get(pk=id)
    appointments.delete()
    return redirect('implant')


def home(request):
    return render(request, 'home.html')


def home1(request):
    return render(request, 'home1.html')


def contact(request):
    if request.method =='POST':
       form = ContactForm(request.POST)
       if form.is_valid():
           name = form.cleaned_data['name']
           email = form.cleaned_data['email']
           subject = form.cleaned_data['subject']
           message = form.cleaned_data['message']
           form.save()
           send_mail(subject,message,settings.EMAIL_HOST_USER,[email])
           return render(request, 'contact.html',{'form':form})
    else:
        form = ContactForm()
        return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def doctors(request):
    return render(request, 'doctors.html')


def appointment1(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            date = form.cleaned_data['date']
            phone = form.cleaned_data['phone']
            form.save()
            send_mail(name, email, address, ['aabduljabar@swedoaid.org'])
            appointments = Appointment1.objects.all()
            return render(request, 'appointment1.html', {'form': form,'appointments':appointments})
    else:
        form = AppointmentForm()

        return render(request, 'appointment1.html')


def all_appo(request):
    appointments = Appointment1.objects.all().order_by('-id')
    return render(request, 'all_appo.html', {'appointments': appointments})


def dentist_details(request, id):
    if request.method ==  'POST':
        form = DentistDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all-details')
    else:

        form = DentistDetailsForm(request.POST)
        appointments = Appointment1.objects.all().order_by('-id')
        return render(request,'dentist_details.html',{'form':form,'appointments': appointments})


def all_details(request):
    appointments = DentistDetails.objects.all().order_by('-id')
    return render(request, 'all_details.html', {'appointments': appointments})


def update(request, id):
    pi = DentistDetails.objects.get(pk=id)
    form = DentistDetailsForm(request.POST or None,  instance=pi)
    if form.is_valid():
        form.save()
        return redirect('all-details')
    return render(request,'update.html',{'form':form,'pi':pi})


def delete_details(request, id):
    venue = DentistDetails.objects.get(pk=id)
    venue.delete()
    return redirect('all-details')


def search_details(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        venues = DentistDetails.objects.filter(idappointment__name__icontains=searched)
        appointments = Appointment1.objects.all()
        return render(request, 'search_details.html', {'searched': searched, 'venues': venues, 'appointments': appointments})
    else:
        return render(request, 'search_details.html', {})


def search_appo(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        venues = Appointment1.objects.filter(name__icontains=searched)
        appointments = Appointment1.objects.all()
        return render(request, 'search_appo.html', {'searched': searched, 'venues': venues, 'appointments': appointments})
    else:
        return render(request, 'search_appo.html', {})


def reception(request):
    if request.method == 'POST':
        form = ReceptionForm(request.POST)
        if form.is_valid():
            # Get the currently logged-in user
            user = request.user
            instance = form.save(commit=False)
            instance.user = user  # Associate the Reception instance with the logged-in user

            doctor_name = form.cleaned_data['doctor']
            educational_name = form.cleaned_data['educational']
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            instance.doctor = Doctors.objects.get(doctor_name=doctor_name)


            try:
                educational_instance = Educational.objects.get(educational_name=educational_name)
            except Educational.DoesNotExist:
                educational_instance = None

            instance.educational = educational_instance

            app_data = request.POST.get('app_data')
            days = request.POST.get('days')
            selected_times = request.POST.getlist('time')

            if Reception.objects.filter(doctor=instance.doctor, educational=instance.educational,
                                        app_data=app_data, days=days, time=selected_times).exists():
                messages.error(request, f'This date, days, and time are already booked for {doctor_name}.<br/> You Can Choose another Time')
                return redirect('home')

            instance.app_data = app_data
            instance.days = days
            instance.time = selected_times
            instance.save()

            # Save the same data to Reception1 model
            Reception1.objects.create(
                name=name,
                phone=phone,
                gender =gender,
                date_of_birth=date_of_birth,
                app_data=app_data,
                days=days,
                time=selected_times,
                doctor=instance.doctor,
                educational=instance.educational,
                idReception_id=instance.id,  # Assigning the id of Reception instance
                user_id=user.id

            )

            selected_times_str = ', '.join(selected_times)
            messages.success(request, f'Appointment successfully booked for {name}, {app_data}, {days}, at {selected_times_str}.')
            return redirect('home')

    else:
        form = ReceptionForm()

    appointments = Reception.objects.all().order_by('-id')
    cleaned_appointments = []
    for appointment in appointments:
        if appointment.days:
            appointment.days = appointment.days.replace("'", "")
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
        cleaned_appointments.append(appointment)

    return render(request, 'home.html', {'form': form, 'appointments': appointments})


def search_doctor(request):
    form = SearchForm()  # Always instantiate the form
    receptions = Reception1.objects.none()  # Initialize as an empty queryset

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    doctor_id = request.GET.get('doctor')

    is_admin = request.user.is_authenticated and request.user.role == 'admin'

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            selected_doctor = form.cleaned_data['doctor']

            # Check if the user is an admin
            if not is_admin and request.user.username != selected_doctor.doctor_name:
                return redirect(reverse('login'))  # Redirect to the login page for non-admin users

            # Filter receptions by the selected doctor
            receptions = Reception1.objects.filter(doctor=selected_doctor)

    else:
        # If start_date and end_date are provided, filter receptions by the date range
        if start_date and end_date:
            # Convert start_date and end_date to datetime objects
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

            # If a doctor is selected, further filter by both doctor and date range
            if doctor_id:
                selected_doctor = get_object_or_404(Doctors, id=doctor_id)
                receptions = Reception.objects.filter(doctor=selected_doctor, app_data__range=(start_datetime, end_datetime))
            else:
                # If no doctor is selected, filter by the date range only
                receptions = Reception1.objects.filter(app_data__range=(start_datetime, end_datetime))

    # Clean appointments data before rendering
    for reception in receptions:
        if reception.days:
            reception.days = reception.days.replace("'", "")
        if reception.time:
            reception.time = reception.time.replace("'", "")

    return render(request, 'doctors/search_doctor.html', {'form': form, 'receptions': receptions, 'start_date': start_date, 'end_date': end_date})


def search_educational(request):
    form = SearchForm1()  # Always instantiate the form
    receptions = Reception1.objects.none()  # Initialize as an empty queryset
    oralls = Ortho.objects.none()  # Initialize as an empty queryset

    if request.method == 'POST':
        form = SearchForm1(request.POST)
        if form.is_valid():
            selected_educational = form.cleaned_data['educational']

            # Check if the user is an admin
            is_admin = request.user.is_authenticated and request.user.role == 'admin'

            # Check if the selected educational's name matches the logged-in user's username
            if not is_admin and request.user.username != selected_educational.educational_name:
                # Instead of redirecting, show an alert using JavaScript
                return render(request, 'doctors/search_educational.html',
                              {'form': form, 'alert_message': 'You do not have permission to access this Data'})

            receptions = Reception1.objects.filter(educational=selected_educational).order_by('-app_data')

            # Assuming idReception is the correct field to link Ortho objects to Reception
            oralls = Ortho.objects.filter(idReception1__in=receptions).order_by('-id')

            # Debug statements
            print("Selected Educational:", selected_educational)
            print("Receptions:", receptions)


    # Clean appointments data before rendering
    for reception in receptions:
        if reception.days:
            reception.days = reception.days.replace("'", "")
        if reception.time:
            reception.time = reception.time.replace("'", "")

    return render(request, 'doctors/search_educational.html', {'form': form, 'receptions': receptions, 'oralls': oralls})


def all_reception(request):

    appointments = Reception1.objects.all().order_by('-id')

    for appointment in appointments:
        if appointment.days:
            appointment.days = appointment.days.replace("'", "")
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")

    return render(request, 'all_reception.html', {'appointments': appointments})


def user_all(request):
    # Assuming the user is logged in
    user = request.user

    # Check if the user is an admin or a patient
    is_admin_or_patient = user.is_authenticated and (user.role == 'admin' or user.role == 'patient')

    # Assuming you have a username and custom_password variable (e.g., passed through the URL)
    username = request.GET.get('username')
    custom_password = request.GET.get('custom_password')

    # Check if the username and custom_password match the logged-in user's credentials
    if is_admin_or_patient and user.username == username and user.custom_password == custom_password:
        # Filter appointments for the patient or admin user
        custom_user = CustomUser.objects.get(pk=user.id)
        appointments = Reception.objects.filter(user_id=custom_user.id).order_by('-id')
        for appointment in appointments:
            if appointment.days:
                appointment.days = appointment.days.replace("'", "")
            if appointment.time:
                appointment.time = appointment.time.replace("'", "")

        return render(request, 'user_all.html', {'appointments': appointments})

    print(f"is_admin_or_patient: {is_admin_or_patient}")
    print(f"username: {username}")
    print(f"custom_password: {custom_password}")
    print(f"user: {user}")
    # Instead of redirecting, show an alert using JavaScript

    # Instead of redirecting, show an alert using JavaScript
    return render(request, 'user_all.html', {'alert_message': 'You do not have permission to access this Data'})


def search_reception(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'search_reception.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'search_reception.html', {})


def search_gave(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        gaves = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'search_gave.html', {'searched': searched, 'gaves': gaves, 'receptions': receptions})
    else:
        return render(request, 'search_gave.html', {})


def delete_reception(request, id):
    # Get the Reception instance
    reception_instance = get_object_or_404(Reception, pk=id)

    # Get the corresponding Reception1 instance (assuming you have a shared identifier)
    reception1_instance = get_object_or_404(Reception1, pk=id)

    # Delete both instances
    reception_instance.delete()
    reception1_instance.delete()

    return redirect('all-reception')


def update_reception(request, id):
    pi = Reception1.objects.get(pk=id)
    form = ReceptionForm1(request.POST or None, instance=pi)
    if form.is_valid():
        form.save()
        return redirect('all-reception')
    return render(request, 'update_reception.html', {'form': form, 'pi': pi})


@login_required
def update_appointment(request, id):
    pi = Reception1.objects.get(pk=id)
    form = ReceptionForm1(request.POST or None, instance=pi)
    if form.is_valid():
        form.save()
        return redirect('user_all')
    return render(request, 'update_appointment.html', {'form': form, 'pi': pi})


def gave_appointment(request, id):
    # Check if the request method is POST
    if request.method == 'POST':
        # Initialize the form with the submitted POST data
        form = ReceptionForm1(request.POST)
        if form.is_valid():
            # Create a new instance of Reception from the form data
            instance = form.save(commit=False)

            # Get the doctor's name from the form's cleaned data
            doctor_name = form.cleaned_data['doctor']
            selected_times = form.cleaned_data['time']

            # Retrieve the corresponding Doctors instance from the database
            instance.doctor = Doctors.objects.get(doctor_name=doctor_name)

            # Get the app_data, days, and time values from the POST data
            app_data = request.POST.get('app_data')
            days = request.POST.get('days')
            time = request.POST.get('time')  # Make sure 'time' is available in the form data

            # Set the user_id, name, and phone for the new instance
            instance.user_id = request.user.id  # Assuming you have access to the user ID
            # Check if the same combination of app_data, days, and time exists in the database
            if Reception1.objects.filter(app_data=app_data, days=days, time=selected_times).exists():
                messages.error(request, 'This date, days, and time are already booked. You can choose another Time.')
                return redirect('gave-appointment', id=id)

            # Retrieve the existing Reception instance with the provided ID
            existing_reception = Reception1.objects.get(id=id)

            # Set the instance fields using existing data and new values
            instance.idReception_id = existing_reception.idReception_id
            instance.gender = existing_reception.gender
            instance.date_of_birth = existing_reception.date_of_birth
            instance.app_data = app_data
            instance.days = days
            instance.time = selected_times
            instance.user_id = existing_reception.user_id

            # Save the new instance to the database
            instance.save()

            # Redirect to 'home' after successful form submission
            messages.success(request, f'Appointment successfully booked for {app_data}, {days}, {selected_times}.')
            return redirect('gave-appointment', id=id)
    else:
        # Retrieve the existing Reception instance with the provided ID
        existing_reception = Reception1.objects.get(id=id)

        # Populate the form with initial data from the existing instance
        initial_data = {
            'idReception': existing_reception.idReception_id,
            'name': existing_reception.name,
            'phone': existing_reception.phone,
            'gender': existing_reception.gender,
            'date_of_birth': existing_reception.date_of_birth,
            'user_id': existing_reception.user_id
        }
        form = ReceptionForm1(initial=initial_data)

    # Retrieve all Reception instances from the database
    appointments = Reception1.objects.all().order_by('-id')

    # Clean appointments data before rendering
    cleaned_appointments = []
    for appointment in appointments:
        if appointment.days:
            appointment.days = appointment.days.replace("'", "")
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
        cleaned_appointments.append(appointment)

    # Render the template with the form and appointments data
    return render(request, 'gave_appointment.html', {'form': form, 'appointments': cleaned_appointments})


def print_appointment(request, id):
    drugs = Reception1.objects.filter(id=id)
    context = {
        'drugs': drugs,
    }
    return render(request, 'print_appointment.html', context)


def all_gave(request):
    # Get current time
    current_time = datetime.now()
    gaves = Reception1.objects.all().order_by('-id')

    # Retrieve 'gave' records within the last 24 hours
    gaves = Reception1.objects.filter(app_data__gte=current_time - timedelta(hours=360)).order_by('-id')

    # Clean 'gave' data if needed
    for gave in gaves:
        if gave.days:
            gave.days = gave.days.replace("'", "")
        if gave.time:
            gave.time = gave.time.replace("'", "")

    return render(request, 'all_gave.html', {'gaves': gaves})


@login_required
def add_oral_surgery(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = OralSurgeryForm(request.POST, request.FILES)
            if form.is_valid():
                oral_surgery = form.save(commit=False)
                implant_name = form.cleaned_data['implant']
                oral_surgery.implant = Implant.objects.get(implant_name=implant_name)
                oral_surgery.idReception1_id = id

                price = form.cleaned_data['price']
                oral_surgery.idReception_id = reception.idReception_id
                oral_surgery.name = reception.name
                oral_surgery.phone = reception.phone
                oral_surgery.gender = reception.gender
                oral_surgery.date_of_birth = reception.date_of_birth
                oral_surgery.educational_id = reception.educational_id
                oral_surgery.doctor_id = reception.doctor_id

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                oral_surgery.doctor_share = doctor_share.quantize(Decimal('0.01'))
                oral_surgery.center_share = center_share.quantize(Decimal('0.01'))
                oral_surgery.price_lab = price_lab_decimal  # Save price_lab as Decimal
                oral_surgery.total_price = total_price.quantize(Decimal('0.01'))  # Save price_lab as Decimal

                oral_surgery.save()

            photos = request.FILES.getlist('exo_images')
            oral_surgery_instance = form.save(commit=False)
            oral_surgery_instance.save()

            for photo in photos:
                Photo.objects.create(oral_surgery_instance=oral_surgery_instance, image=photo)

            return redirect('add-oral-surgery', id=id)
        else:
            initial_data = {
                'idReception1_id': id,
                'name': reception.name,
                'idReception_id': reception.idReception_id,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'doctor_id': reception.doctor_id
            }
            form = OralSurgeryForm(initial=initial_data)
    except Doctors.DoesNotExist:
        return redirect('error_page')

    appointments = Reception1.objects.all().order_by('-id')
    oralls = OralSurgery.objects.filter(idReception1=id)
    photos_list = []

    try:
        orall = oralls.first()
        photos = orall.photo_set.all()
    except AttributeError:
        orall = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None

    for orall in oralls:
        if orall.ur:
            orall.ur = orall.ur.replace("'", "")
        if orall.ul:
            orall.ul = orall.ul.replace("'", "")
        if orall.lr:
            orall.lr = orall.lr.replace("'", "")
        if orall.ll:
            orall.ll = orall.ll.replace("'", "")
        orall.total_price = orall.total_price
        orall.save()
        photos = orall.photo_set.all()
        photos_list.append(photos)

    formatted_total_prices = ["{:,}".format(orall.total_price) if orall.total_price is not None else None for orall in oralls]
    formatted_prices = ["{:,}".format(orall.price) if orall.price is not None else None for orall in oralls]

    return render(request, 'index.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'oralls': oralls,
        'id': id,
        'photos': photos,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


def remove_photo_oral(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    oral_surgery_instance = photo.oral_surgery_instance
    photo.delete()
    return redirect('oral-edit', id=oral_surgery_instance.id)


def delete_oral(request, id):
    # Get the drug related to the Reception
    oral = get_object_or_404(OralSurgery, id=id)

    # Store the idReception before deleting the drug
    idReception = oral.idReception1_id

    # Delete the drug
    oral.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('add-oral-surgery', id=idReception)


def oral_reception(request):
    appointments = Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,25)  # Paginator
    page = request.GET.get('page')  # Paginator
    appointments = p.get_page(page)  # Paginator
    nums = "a" * appointments.paginator.num_pages  # Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'oral_reception.html', {'appointments': appointments})


def search_oral(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'search_oral_surgery.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'search_oral_surgery.html', {})


def oral_edit(request, id):
    orall = get_object_or_404(OralSurgery, id=id)
    photos = Photo.objects.filter(oral_surgery_instance=orall)

    if request.method == 'POST':
        form = OralSurgeryForm(request.POST, request.FILES, instance=orall)
        if form.is_valid():
            print("Form is valid")
            implant_name = form.cleaned_data['implant']
            price = form.cleaned_data['price']
            implant = Implant.objects.get(implant_name=implant_name)
            orall.implant = implant
            form_data = form.cleaned_data

            # Sanitize the fields by removing single quotes
            for field in ['ur', 'ul', 'lr', 'll']:
                form_data[field] = form_data[field].replace("'", "") if form_data[field] else None

            for field, value in form_data.items():
                setattr(orall, field, value)

            try:
                doctor = Doctors.objects.get(id=orall.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab')

            if price_lab is not None:
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price
            else:
                adjusted_price = price

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            orall.doctor_share = doctor_share.quantize(Decimal('0.01'))
            orall.center_share = center_share.quantize(Decimal('0.01'))
            orall.total_price = total_price.quantize(Decimal('0.01'))

            # Handle lab_name separately
            selected_lab = form.cleaned_data['lab_name']
            if selected_lab:
                orall.lab = selected_lab  # Set the foreign key to the selected Lab
                orall.lab_name = selected_lab.lab_name  # Save the lab_name as well
            orall.save()

            photos = request.FILES.getlist('oral_images')
            for photo in photos:
                Photo.objects.create(oral_surgery_instance=orall, image=photo)

            return redirect('add-oral-surgery', id=orall.idReception1_id)
        else:
            print("Form is not valid")
            print(form.errors)

    else:
        # Sanitize initial values for the form fields
        first_visit = orall.first_visit if orall.first_visit is not None else None
        second_visit = orall.second_visit if orall.second_visit is not None else None
        third_visit = orall.third_visit if orall.third_visit is not None else None
        fourth_visit = orall.fourth_visit if orall.fourth_visit is not None else None
        fifth_visit = orall.fifth_visit if orall.fifth_visit is not None else None
        ur = orall.ur[1:-1] if orall.ur else None
        ul = orall.ul[1:-1] if orall.ul else None
        lr = orall.lr[1:-1] if orall.lr else None
        ll = orall.ll[1:-1] if orall.ll else None

        form = OralSurgeryForm(instance=orall, initial={
            'first_visit': first_visit,
            'second_visit': second_visit,
            'third_visit': third_visit,
            'fourth_visit': fourth_visit,
            'fifth_visit': fifth_visit,
            'ur': ur,
            'ul': ul,
            'lr': lr,
            'll': ll,
        })

    labs = Lab.objects.all()
    return render(request, 'update_oral_surgery.html', {'form': form, 'orall': orall, 'labs': labs,'photos':photos})


def oral_visit(request, id):
    orall = get_object_or_404(OralSurgery, id=id)

    if request.method == 'POST':
        form = OralSurgeryForm(request.POST, instance=orall)
        if form.is_valid():
            # Update the implant field based on the selected implant
            implant_name = form.cleaned_data['implant']
            implant = Implant.objects.get(implant_name=implant_name)
            orall.implant = implant
            # Replace single quotes in certain fields
            if orall.ur:
                orall.ur = orall.ur.replace("'", "")
            if orall.ul:
                orall.ul = orall.ul.replace("'", "")
            if orall.lr:
                orall.lr = orall.lr.replace("'", "")
            if orall.ll:
                orall.ll = orall.ll.replace("'", "")

            form.save()
            return redirect('add-oral-surgery', id=orall.idReception_id)
    else:
        # Define a default value for first_visit when the request method is not POST
        first_visit = orall.first_visit if orall.first_visit else date.today()
        # Define a default value for second_visit when the request method is not POST
        second_visit = orall.second_visit if orall.second_visit is not None else None
        third_visit = orall.third_visit if orall.third_visit is not None else None
        fourth_visit = orall.fourth_visit if orall.fourth_visit is not None else None
        fifth_visit = orall.fifth_visit if orall.fifth_visit is not None else None
        # Remove first and last characters from certain fields
        ur = orall.ur[1:-1] if orall.ur else None
        ul = orall.ul[1:-1] if orall.ul else None
        lr = orall.lr[1:-1] if orall.lr else None
        ll = orall.ll[1:-1] if orall.ll else None

        form = OralSurgeryForm(instance=orall, initial={
            'second_visit': second_visit,
            'third_visit': third_visit,
            'fourth_visit': fourth_visit,
            'fifth_visit': fifth_visit,
            'ur': ur,
            'ul': ul,
            'lr': lr,
            'll': ll,
        })

    return render(request, 'oral_visit.html', {'form': form, 'orall': orall, 'first_visit': first_visit})


def all_oral_surgery(request):
    orals = OralSurgery.objects.all().order_by('-id')
    return render(request, 'all_oral_surgery.html', {'orals': orals})


def visit(request):
    if request.method == 'POST':
        form = VisitsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visit')  # Redirect to the same page after saving the form data
    else:
        form = VisitsForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Visits.objects.all().order_by('-id')
    return render(request, 'ortho/visit.html', {'form': form, 'appointments': appointments})


def delete_visit(request,id):
    appointments = Visits.objects.get(pk=id)
    appointments.delete()
    return redirect('visit')




@login_required
def add_ortho(request, id):
    disable_submit = False
    orall = None  # Initialize orall outside try-except block

    try:
        user = request.user

        # Check if the user is an admin or the doctor associated with the reception
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            doctor = Doctors.objects.get(user=user)
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = OrthoForm(request.POST, request.FILES)
            if form.is_valid():
                ortho = form.save(commit=False)
                ortho.idReception1_id = id
                ortho.idReception_id = reception.idReception_id
                ortho.name = reception.name
                ortho.phone = reception.phone
                ortho.gender = reception.gender
                ortho.date_of_birth = reception.date_of_birth
                ortho.educational_id = reception.educational_id
                ortho.doctor_id = reception.doctor_id

                # Calculate total price and shares
                price = form.cleaned_data['price']

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")
                # Assign Decimal values to model fields
                ortho.doctor_share = doctor_share.quantize(Decimal('0.01'))
                ortho.center_share = center_share.quantize(Decimal('0.01'))
                ortho.total_price = total_price.quantize(Decimal('0.01'))
                ortho.price_lab = price_lab_decimal  # Save price_lab as Decimal
                ortho.save()

                # Handle uploaded photos
                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(ortho_instance=ortho, image=photo)

                # Set disable_submit flag to True after successful form processing
                disable_submit = True

                return redirect('add-ortho', id=id)

        else:
            initial_data = {
                'idReception1_id': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'doctor_id': reception.doctor_id,
            }
            form = VeneerForm(initial=initial_data)

    except (ObjectDoesNotExist, ValueError):
        reception = None
        form = None

    # Retrieve Ortho objects related to the current reception
    oralls_with_visits = Ortho.objects.filter(idReception1=id, visits_id__isnull=False).order_by('-id')
    oralls_without_visits = Ortho.objects.filter(idReception1=id, visits_id__isnull=True).order_by('-id')
    oralls = oralls_with_visits.union(oralls_without_visits)
    photos_list = []

    for orall in oralls:
        # Clean up certain fields
        for field in ['ur', 'ul', 'lr', 'll', 'urn', 'uln', 'lrn', 'lln', 'teeth_type', 'urs', 'uls', 'lrs', 'lls', 'teeth_size']:
            value = getattr(orall, field)
            if value:
                setattr(orall, field, value.replace("'", ""))

        orall.save()

        # Retrieve photos associated with the current Ortho instance
        photos = orall.photo_set.all()
        photos_list.append(photos)

    # Retrieve other related data
    appointments = Reception1.objects.all().order_by('-id')
    # Format total prices and prices
    formatted_total_prices = ["{:,}".format(orall.total_price) if orall.total_price is not None else None for orall in oralls]
    formatted_prices = ["{:,}".format(orall.price) if orall.price is not None else None for orall in oralls]

    # Ensure to handle the case where oralls might be empty
    orall = None
    if oralls.exists():
        orall = oralls.first()  # Get the first Orall instance if any


    return render(request, 'ortho/ortho.html', {
        'form': form,
        'appointments': appointments,
        'medicine': None,  # Adjust this based on your logic
        'oralls': oralls,
        'id': id,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices,
        'disable_submit': disable_submit,
        'orall': orall,  # Ensure to pass the last orall outside the loop correctly
    })


def start_ortho(request, id):
    orall = get_object_or_404(Ortho, id=id)

    if request.method == 'POST':
        form = OrthoForm(request.POST, request.FILES, instance=orall)
        if form.is_valid():
            if orall.urs:
                orall.urs = orall.urs.replace("'", "")
            if orall.uls:
                orall.uls = orall.uls.replace("'", "")
            if orall.lrs:
                orall.lrs = orall.lrs.replace("'", "")
            if orall.lls:
                orall.lls = orall.lls.replace("'", "")
            if orall.teeth_type:
                orall.teeth_type = orall.teeth_type.replace("'", "")
            if orall.teeth_size:
                orall.teeth_size = orall.teeth_size.replace("'", "")

                # Saving the form and assigning total_price
            ortho_instance = form.save(commit=False)
            price = form.cleaned_data['price']
            total_price = price  # Initially, total_price is just the price itself
            ortho_instance.total_price = total_price
            ortho_instance.save()
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(ortho_instance=ortho_instance, image=photo)

            price = form.cleaned_data['price']
            total_price = price  # Initially, total_price is just the price itself
            ortho_instance.total_price = total_price
            return redirect('add-ortho', id=orall.idReception_id)
    else:
        # Remove first and last characters from certain fields
        urs = orall.urs[1:-1] if orall.urs else None
        uls = orall.uls[1:-1] if orall.uls else None
        lrs = orall.lrs[1:-1] if orall.lrs else None
        lls = orall.lls[1:-1] if orall.lls else None
        # Add the code to remove the first and last characters from certain fields
        ur = orall.ur[1:-1] if orall.ur else None
        ul = orall.ul[1:-1] if orall.ul else None
        lr = orall.lr[1:-1] if orall.lr else None
        ll = orall.ll[1:-1] if orall.ll else None
        urn = orall.urn[1:-1] if orall.urn else None
        uln = orall.uln[1:-1] if orall.uln else None
        lrn = orall.lrn[1:-1] if orall.lrn else None
        lln = orall.lln[1:-1] if orall.lln else None
        teeth_type = orall.teeth_type[1:-1] if orall.teeth_type else None
        teeth_size = orall.teeth_size[1:-1] if orall.teeth_size else None

        form = OrthoForm(instance=orall, initial={
            'urs': urs,
            'uls': uls,
            'lrs': lrs,
            'lls': lls,
            'ur': ur,
            'ul': ul,
            'lr': lr,
            'll': ll,
            'urn': urn,
            'uln': uln,
            'lrn': lrn,
            'lln': lln,
            'teeth_type': teeth_type,
            'teeth_size': teeth_size,
        })

    return render(request, 'ortho/start_ortho.html', {'form': form, 'orall': orall})


def ortho_visit(request, id):
    orall = get_object_or_404(Ortho, id=id)

    if request.method == 'POST':
        form = OrthoForm(request.POST, instance=orall)
        if form.is_valid():
            form.save()
            return redirect('add-ortho', id=orall.idReception_id)
    else:
        form = OrthoForm(instance=orall)

    return render(request, 'ortho/ortho_visit.html', {'form': form, 'orall': orall})


def ortho_edit(request, id):
    orall = get_object_or_404(Ortho, id=id)
    photos = Photo.objects.filter(ortho_instance=orall)

    if request.method == 'POST':
        form = OrthoForm(request.POST, request.FILES, instance=orall)
        if form.is_valid():
            ortho = form.save(commit=False)
            price = form.cleaned_data['price']
            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            price = Decimal(price)
            ortho.price = price



            try:
                doctor = Doctors.objects.get(id=orall.idReception1.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = Decimal('0')
            else:
                # Default case if no valid discount_option is selected
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            # Set formatted values
            ortho.doctor_share = doctor_share.quantize(Decimal('0.01'))
            ortho.center_share = center_share.quantize(Decimal('0.01'))
            ortho.total_price = total_price.quantize(Decimal('0.01'))
            ortho.price_lab = price_lab_decimal

            # Handle lab_name separately
            selected_lab = form.cleaned_data.get('lab_name')
            if selected_lab:
                ortho.lab = selected_lab  # Set the foreign key to the selected Lab
                ortho.lab_name = selected_lab.lab_name  # Save the lab_name as well

            ortho.save()

            # Handle saving of associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(ortho_instance=orall, image=photo)

            return redirect('add-ortho', id=orall.idReception1_id)
        else:
            print("Form is not valid:", form.errors)
    else:
        form = OrthoForm(instance=orall)

    labs = Lab.objects.all()
    return render(request, 'ortho/update_ortho.html', {'form': form, 'orall': orall, 'photos': photos, 'labs': labs})


def ortho_edit_visit(request, id):
    # Retrieve the Ortho instance based on the provided ID
    orall = get_object_or_404(Ortho, id=id)
    # Retrieve associated photos
    photos = Photo.objects.filter(ortho_instance=orall)

    if request.method == 'POST':
        # Bind the form with POST data and the existing Ortho instance
        form = OrthoForm(request.POST, request.FILES, instance=orall)

        if form.is_valid():
            # Extract cleaned data
            price = form.cleaned_data['price']
            visits = form.cleaned_data['visits']
            total_price = price  # This might be used to update some total price field

            # Update the Ortho instance with cleaned data
            orall = form.save(commit=False)
            orall.total_price = total_price
            orall.visits = visits

            # Ensure lab_name is correctly set
            if form.cleaned_data['lab_name']:
                orall.lab_name = form.cleaned_data['lab_name']
            else:
                orall.lab_name = orall.lab_name
            orall.save()

            # Handle the saving of associated photos
            if 'exo_images' in request.FILES:
                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(ortho_instance=orall, image=photo)

            print("Form submission successful. Redirecting...")
            return redirect('add-ortho', id=orall.idReception1_id)
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        # Initialize the form with the existing Ortho instance
        form = OrthoForm(instance=orall, initial={
            'lab_name': orall.lab_name  # Ensure this sets the initial value
        })

    print("Rendering ortho_edit_visit template...")
    return render(request, 'ortho/ortho_edit_visit.html', {'form': form, 'orall': orall, 'photos': photos})


def ortho_visit1(request, id):
    orall = get_object_or_404(Ortho, id=id)
    all_oralls = Ortho.objects.filter(idReception1=orall.idReception1).order_by('-id')
    if request.method == 'POST':

        # Create a new instance of Ortho
        new_orall = Ortho()

        # Copy data from the existing orall object to the new instance
        new_orall.idReception = orall.idReception
        new_orall.idReception1 = orall.idReception1
        new_orall.name = orall.name
        new_orall.phone = orall.phone
        new_orall.gender = orall.gender
        new_orall.date_of_birth = orall.date_of_birth
        new_orall.educational_id = orall.educational_id
        new_orall.doctor_id = orall.doctor_id
        new_orall.ur = orall.ur
        new_orall.ul = orall.ul
        new_orall.lr = orall.lr
        new_orall.ll = orall.ll
        new_orall.urn = orall.urn
        new_orall.uln = orall.uln
        new_orall.lrn = orall.lrn
        new_orall.lln = orall.lln
        new_orall.teeth_type = orall.teeth_type
        new_orall.angle_class = orall.angle_class
        new_orall.over_jet = orall.over_jet
        new_orall.over_bt = orall.over_bt
        new_orall.jow_shift = orall.jow_shift
        new_orall.midlin_shift = orall.midlin_shift
        new_orall.urs = orall.urs.replace("'", "") if orall.urs else None
        new_orall.uls = orall.uls.replace("'", "") if orall.uls else None
        new_orall.lrs = orall.lrs.replace("'", "") if orall.lrs else None
        new_orall.lls = orall.lls.replace("'", "") if orall.lls else None
        new_orall.teeth_size = orall.teeth_size.replace("'", "") if orall.teeth_size else None
        new_orall.SNA_before = orall.SNA_before
        new_orall.SNA_after = orall.SNA_after
        new_orall.SNB_before = orall.SNB_before
        new_orall.SNB_after = orall.SNB_after
        new_orall.ANB_before = orall.ANB_before
        new_orall.ANB_after = orall.ANB_after
        new_orall.IMPA_before = orall.IMPA_before
        new_orall.IMPA_after = orall.IMPA_after
        new_orall.U1_SN_before = orall.U1_SN_before
        new_orall.U1_SN_after = orall.U1_SN_after
        new_orall.SNGOGN_before = orall.SNGOGN_before
        new_orall.SNGOGN_after = orall.SNGOGN_after
        new_orall.treatment_plan = orall.treatment_plan
        new_orall.price = orall.price
        new_orall.paid = orall.paid
        new_orall.discount_option = orall.discount_option
        new_orall.lab_name = orall.lab_name
        new_orall.price_lab = orall.price_lab
        new_orall.center_share = orall.center_share
        new_orall.doctor_share = orall.doctor_share
        new_orall.notes = orall.notes
        new_orall.exo_images = orall.exo_images
        new_orall.uper_date = orall.uper_date
        new_orall.lower_date = orall.lower_date
        new_orall.both_date = orall.both_date
        new_orall.discount_option = orall.discount_option

        form = OrthoForm(request.POST, request.FILES, instance=new_orall)
        if form.is_valid():
            # Handle the saving of the form
            new_orall = form.save(commit=False)

            # Ensure lab_name is correctly set
            if form.cleaned_data['lab_name']:
                new_orall.lab_name = form.cleaned_data['lab_name']
            else:
                new_orall.lab_name = orall.lab_name

            # Save the new Ortho object
            new_orall.save()
            photos = request.FILES.getlist('exo_images')

            for photo in photos:
                Photo.objects.create(ortho_instance=new_orall, image=photo)

            return redirect('add-ortho', id=orall.idReception1_id)

    else:
        # Remove first and last characters from certain fields
        urs = orall.urs[1:-1] if orall.urs else None
        uls = orall.uls[1:-1] if orall.uls else None
        lrs = orall.lrs[1:-1] if orall.lrs else None
        lls = orall.lls[1:-1] if orall.lls else None
        ur = orall.ur[1:-1] if orall.ur else None
        ul = orall.ul[1:-1] if orall.ul else None
        lr = orall.lr[1:-1] if orall.lr else None
        ll = orall.ll[1:-1] if orall.ll else None
        urn = orall.urn[1:-1] if orall.urn else None
        uln = orall.uln[1:-1] if orall.uln else None
        lrn = orall.lrn[1:-1] if orall.lrn else None
        lln = orall.lln[1:-1] if orall.lln else None
        teeth_type = orall.teeth_type[1:-1] if orall.teeth_type else None
        teeth_size = orall.teeth_size[1:-1] if orall.teeth_size else None

        form = OrthoForm(instance=orall, initial={
            'urs': urs,
            'uls': uls,
            'lrs': lrs,
            'lls': lls,
            'ur': ur,
            'ul': ul,
            'lr': lr,
            'll': ll,
            'urn': urn,
            'uln': uln,
            'lrn': lrn,
            'lln': lln,
            'teeth_type': teeth_type,
            'teeth_size': teeth_size,
            'lab_name': orall.lab_name

        })
        # Get all instances related to the idReception
        all_oralls = Ortho.objects.filter(idReception1=orall.idReception1).order_by('-id')
        oralls = Ortho.objects.filter(idReception1=id)
        try:
            orall = oralls.first()
        except AttributeError:
            orall = None

    return render(request, 'ortho/ortho_visit1.html', {'form': form,'all_oralls':all_oralls,'orall': orall})


def remove_photo_ortho(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    ortho_instance = photo.ortho_instance
    photo.delete()
    return redirect('ortho-edit', id=ortho_instance.id)

@login_required
def delete_ortho(request, id):
    # Get the drug related to the Reception
    orall = get_object_or_404(Ortho, id=id)

    # Store the idReception before deleting the drug
    idReception = orall.idReception1_id

    # Delete the drug
    orall.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('add-ortho', id=idReception)


def ortho_reception(request):
    appointments = Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,25) #Paginator
    page = request.GET.get('page') #Paginator
    appointments = p.get_page(page)#Paginator
    nums = "a" * appointments.paginator.num_pages#Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'ortho/ortho_reception.html', {'appointments': appointments})


def search_ortho(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'ortho/search_ortho.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'ortho/search_ortho.html', {})


@login_required
def exo_reception(request):
    user = request.user
    try:
        if user.role == 'admin':
            appointments = Reception1.objects.all().order_by('-id')
        else:
            doctor = Doctors.objects.get(user=user)
            appointments = Reception1.objects.filter(doctor=doctor).order_by('-id')
    except Doctors.DoesNotExist:
        appointments = Reception1.objects.none()

    p = Paginator(appointments, 25)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")

    return render(request, 'exo/exo_reception.html', {'appointments': appointments, 'nums': nums})


def prosthodontics_reception(request):
    appointments =Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,25) #Paginator
    page = request.GET.get('page') #Paginator
    appointments = p.get_page(page)#Paginator
    nums = "a" * appointments.paginator.num_pages#Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'prosthodontics/prosthodontics_reception.html', {'appointments': appointments})


def exo_reception1(request):
    appointments =Reception1.objects.all().order_by('-id')
    return render(request, 'exo/exo_reception1.html', {'appointments': appointments})


@login_required
def exo(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = ExoForm(request.POST, request.FILES)
            if form.is_valid():
                oral_surgery = form.save(commit=False)
                oral_surgery.idReception1_id = id

                price = form.cleaned_data['price']
                oral_surgery.name = reception.name
                oral_surgery.phone = reception.phone
                oral_surgery.gender = reception.gender
                oral_surgery.date_of_birth = reception.date_of_birth
                oral_surgery.educational_id = reception.educational_id
                oral_surgery.idReception_id = reception.idReception_id
                oral_surgery.doctor_id = reception.doctor_id

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                oral_surgery.doctor_share = doctor_share.quantize(Decimal('0.01'))
                oral_surgery.center_share = center_share.quantize(Decimal('0.01'))
                oral_surgery.price_lab = price_lab_decimal.quantize(Decimal('0.01'))
                oral_surgery.total_price = total_price.quantize(Decimal('0.01'))  # Save total_price as Decimal

                # Debugging statement to confirm the assignment
                print(f"Total price after quantize: {oral_surgery.total_price}")

                oral_surgery.save()

                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(exo_instance=oral_surgery, image=photo)

                return redirect('exo', id=id)
            else:
                form = ExoForm(initial={
                    'idReception1_id': id,
                    'name': reception.name,
                    'phone': reception.phone,
                    'gender': reception.gender,
                    'date_of_birth': reception.date_of_birth,
                    'educational_id': reception.educational_id,
                    'idReception_id': reception.idReception_id,
                    'doctor_id': reception.doctor_id
                })
        else:
            form = ExoForm(initial={
                'idReception1_id': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'idReception_id': reception.idReception_id,
                'doctor_id': reception.doctor_id
            })

        appointments = Reception1.objects.all().order_by('-id')
        exooes = Exo.objects.filter(idReception1=id)
        photos_list = []

        exoo = exooes.first()
        photos = exoo.photo_set.all() if exoo else None

        medicine = Medicin.objects.filter(idReception=id).first()

        for exoo in exooes:
            if exoo.ur:
                exoo.ur = exoo.ur.replace("'", "")
            if exoo.ul:
                exoo.ul = exoo.ul.replace("'", "")
            if exoo.lr:
                exoo.lr = exoo.lr.replace("'", "")
            if exoo.ll:
                exoo.ll = exoo.ll.replace("'", "")
            if exoo.exoby:
                exoo.exoby = exoo.exoby.replace("'", "")
            if exoo.simpleexo:
                exoo.simpleexo = exoo.simpleexo.replace("'", "")
            if exoo.complcated:
                exoo.complcated = exoo.complcated.replace("'", "")
            exoo.total_price = exoo.total_price
            exoo.save()
            photos = exoo.photo_set.all()
            photos_list.append(photos)

        formatted_total_prices = ["{:,}".format(exoo.total_price) if exoo.total_price is not None else None for exoo in exooes]
        formatted_prices = ["{:,}".format(exoo.price) if exoo.price is not None else None for exoo in exooes]

        return render(request, 'exo/exo.html', {
            'form': form,
            'appointments': appointments,
            'medicine': medicine,
            'exooes': exooes,
            'id': id,
            'photos': photos,
            'photos_list': photos_list,
            'formatted_total_prices': formatted_total_prices,
            'reception': reception,
            'formatted_prices': formatted_prices
        })
    except Doctors.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    except Reception1.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'Reception does not exist or you do not have permission to access it.')
        return redirect('home')


def exo_edit(request, id):
    exoo = get_object_or_404(Exo, id=id)
    photos = Photo.objects.filter(exo_instance=exoo)

    if request.method == 'POST':
        form = ExoForm(request.POST, request.FILES, instance=exoo)
        if form.is_valid():
            exoo = form.save(commit=False)
            price = form.cleaned_data['price']

            try:
                doctor = Doctors.objects.get(id=exoo.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            exoo.doctor_share = doctor_share.quantize(Decimal('0.01'))
            exoo.center_share = center_share.quantize(Decimal('0.01'))
            exoo.total_price = total_price.quantize(Decimal('0.01'))
            exoo.save()

            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(exo_instance=exoo, image=photo)

            return redirect('exo', id=exoo.idReception1_id)
    else:
        form = ExoForm(instance=exoo)

    labs = Lab.objects.all()
    return render(request, 'exo/exo_edit.html', {'form': form, 'id': id, 'exoo': exoo, 'photos': photos, 'labs': labs})


def remove_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    exo_instance = photo.exo_instance
    photo.delete()
    return redirect('exo_edit', id=exo_instance.id)


def prosthodontics_edit(request, id):
    exoo = get_object_or_404(Prosthodontics, id=id)
    photos = Photo.objects.filter(prosthodontics_instance=exoo)  # Fetch photos associated with the oral surgery instance
    if request.method == 'POST':
        form = ProsthodonticsForm(request.POST, request.FILES, instance=exoo)
        if form.is_valid():
            price = form.cleaned_data['price']
            try:
                doctor = Doctors.objects.get(id=exoo.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            # Assign Decimal values to model fields
            form.instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
            form.instance.center_share = center_share.quantize(Decimal('0.01'))
            form.instance.total_price = total_price.quantize(Decimal('0.01'))
            form.instance.price_lab = price_lab_decimal  # Save price_lab as Decimal
            # Handle lab_name separately
            selected_lab = form.cleaned_data['lab_name']
            if selected_lab:
                form.lab = selected_lab  # Set the foreign key to the selected Lab
                form.lab_name = selected_lab.lab_name  # Save the lab_name as well
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(prosthodontics_instance=exoo, image=photo)

            return redirect('prosthodontics', id=exoo.idReception1_id)
    else:
        form = ProsthodonticsForm(instance=exoo)
        try:
            exoo = Prosthodontics.objects.get(idReception1=id)
            photos = exoo.photo_set.all()
            # Sanitize field values in the instance
            if exoo.ur:
                exoo.ur = exoo.ur.replace("'", "")
            if exoo.ul:
                exoo.ul = exoo.ul.replace("'", "")
            if exoo.lr:
                exoo.lr = exoo.lr.replace("'", "")
            if exoo.ll:
                exoo.ll = exoo.ll.replace("'", "")
            if exoo.denture:
                exoo.denture = exoo.denture.replace("'", "")
            if exoo.upper:
                exoo.upper = exoo.upper.replace("'", "")
            if exoo.lower:
                exoo.lower = exoo.lower.replace("'", "")
            if exoo.partial:
                exoo.partial = exoo.partial.replace("'", "")
        except Prosthodontics.DoesNotExist:
            exoo = None
            photos = None
    labs = Lab.objects.all()
    return render(request, 'prosthodontics/prosthodontics_edit.html', {'form': form, 'id': id, 'exoo': exoo, 'photos': photos, 'labs': labs})


def remove_photo_prosthodontics(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    prosthodontics_instance = photo.prosthodontics_instance
    photo.delete()
    return redirect('prosthodontics_edit', id=prosthodontics_instance.id)


def delete_prosthodontics(request, id):
    # Get the drug related to the Reception
    exo = get_object_or_404(Prosthodontics, id=id)

    # Store the idReception before deleting the drug
    idReception = exo.idReception1_id

    # Delete the drug
    exo.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('prosthodontics', id=idReception)


@login_required
def prosthodontics(request, id):
    user = request.user

    # Check if the user is an admin or the doctor associated with the reception
    if user.role == 'admin':
        reception = get_object_or_404(Reception1, id=id)
    else:
        doctor = Doctors.objects.get(user=user)
        reception = get_object_or_404(Reception1, id=id, doctor=doctor)

    if request.method == 'POST':
        form = ProsthodonticsForm(request.POST, request.FILES)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception1_id = id

            price = form.cleaned_data['price']
            price = Decimal(price)  # Convert price to Decimal


            oral_surgery.idReception_id = reception.idReception_id
            oral_surgery.name = reception.name
            oral_surgery.phone = reception.phone
            oral_surgery.gender = reception.gender
            oral_surgery.date_of_birth = reception.date_of_birth
            oral_surgery.educational_id = reception.educational_id
            oral_surgery.doctor_id = reception.doctor_id


            try:
                doctor = Doctors.objects.get(id=reception.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            # Assign Decimal values to model fields
            oral_surgery.doctor_share = doctor_share.quantize(Decimal('0.01'))
            oral_surgery.center_share = center_share.quantize(Decimal('0.01'))
            oral_surgery.total_price = total_price.quantize(Decimal('0.01'))
            oral_surgery.price_lab = price_lab_decimal  # Save price_lab as Decimal

            oral_surgery.save()

            # Handle file uploads
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(prosthodontics_instance=oral_surgery, image=photo)

            return redirect('prosthodontics', id=id)
        else:
            print("Form is not valid:", form.errors)
    else:
        reception = Reception1.objects.get(id=id)
        initial_data = {
            'idReception1_id': id,
            'idReception_id': reception.idReception_id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth,
            'educational_id': reception.educational_id,
            'doctor_id': reception.doctor_id
        }
        form = ProsthodonticsForm(initial=initial_data)

    appointments = Reception1.objects.all().order_by('-id')
    exooes = Prosthodontics.objects.filter(idReception1=id)
    photos_list = []

    try:
        exoo = exooes.first()
        photos = exoo.photo_set.all()
    except AttributeError:
        exoo = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None

    for exoo in exooes:
        if exoo.ur:
            exoo.ur = exoo.ur.replace("'", "")
        if exoo.ul:
            exoo.ul = exoo.ul.replace("'", "")
        if exoo.lr:
            exoo.lr = exoo.lr.replace("'", "")
        if exoo.ll:
            exoo.ll = exoo.ll.replace("'", "")
        if exoo.denture:
            exoo.denture = exoo.denture.replace("'", "")
        if exoo.upper:
            exoo.upper = exoo.upper.replace("'", "")
        if exoo.lower:
            exoo.lower = exoo.lower.replace("'", "")
        if exoo.partial:
            exoo.partial = exoo.partial.replace("'", "")
        exoo.total_price = exoo.total_price
        exoo.save()
        photos = exoo.photo_set.all()
        photos_list.append(photos)

    formatted_total_prices = [
        "{:,.2f}".format(exoo.total_price) if exoo.total_price is not None else None
        for exoo in exooes
    ]
    formatted_prices = [
        "{:,.2f}".format(exoo.price) if exoo.price is not None else None
        for exoo in exooes
    ]

    return render(request, 'prosthodontics/prosthodontics.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'exooes': exooes,
        'id': id,
        'photos': photos,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


def search_periodontology(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'periodontology/search_periodontology.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'periodontology/search_periodontology.html', {})


def remove_photo_periodontology(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    periodontology_instance = photo.periodontology_instance
    photo.delete()
    return redirect('periodontology_edit', id=periodontology_instance.id)


def delete_periodontology(request, id):
    # Get the drug related to the Reception
    exo = get_object_or_404(Periodontology, id=id)

    # Store the idReception before deleting the drug
    idReception = exo.idReception1_id

    # Delete the drug
    exo.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('periodontology', id=idReception)


@login_required
def periodontology(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = PeriodontologyForm(request.POST, request.FILES)
            if form.is_valid():
                oral_surgery = form.save(commit=False)
                oral_surgery.idReception1_id = id

                price = form.cleaned_data['price']
                oral_surgery.name = reception.name
                oral_surgery.phone = reception.phone
                oral_surgery.gender = reception.gender
                oral_surgery.date_of_birth = reception.date_of_birth
                oral_surgery.educational_id = reception.educational_id
                oral_surgery.doctor_id = reception.doctor_id

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                oral_surgery.doctor_share = doctor_share.quantize(Decimal('0.01'))
                oral_surgery.center_share = center_share.quantize(Decimal('0.01'))
                oral_surgery.price_lab = price_lab_decimal  # Save price_lab as Decimal
                oral_surgery.total_price = total_price.quantize(Decimal('0.01'))
                oral_surgery.save()

                # Save photos associated with the oral_surgery instance
                for photo in request.FILES.getlist('exo_images'):
                    Photo.objects.create(periodontology_instance=oral_surgery, image=photo)

                return redirect('periodontology', id=id)
        else:
            # Populate initial form data when the request method is GET
            initial_data = {
                'idReception1': id,
                'idReception': reception.idReception_id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'doctor_id': reception.doctor_id
            }
            form = PeriodontologyForm(initial=initial_data)
    except (ObjectDoesNotExist, Doctors.DoesNotExist):
        # Handle case where Reception1 or Doctors do not exist
        # This could happen if the id does not exist or user's doctor record is missing
        initial_data = {
            'idReception1': id,
            'idReception': reception.idReception_id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth,
            'educational_id': reception.educational_id,
            'doctor_id': reception.doctor_id
        }
        form = PeriodontologyForm(initial=initial_data)

    # Fetch data for rendering the template
    appointments = Reception1.objects.all().order_by('-id')
    exooes = Periodontology.objects.filter(idReception1=id)
    photos_list = []

    try:
        exoo = exooes.first()
        photos = exoo.photo_set.all()
    except AttributeError:
        exoo = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None

    for exoo in exooes:
        if exoo.type:
            exoo.type = exoo.type.replace("'", "")
        exoo.total_price = exoo.total_price
        exoo.save()
        photos = exoo.photo_set.all()
        photos_list.append(photos)

    formatted_total_prices = ["{:,}".format(exoo.total_price) if exoo.total_price is not None else None for exoo in exooes]
    formatted_prices = ["{:,}".format(exoo.price) if exoo.price is not None else None for exoo in exooes]

    return render(request, 'periodontology/periodontology.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'exooes': exooes,
        'id': id,
        'photos': photos,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


def periodontology_edit(request, id):
    exoo = get_object_or_404(Periodontology, id=id)
    photos = Photo.objects.filter(
        periodontology_instance=exoo)  # Fetch photos associated with the periodontology instance

    if request.method == 'POST':
        form = PeriodontologyForm(request.POST, request.FILES, instance=exoo)
        if form.is_valid():
            price = form.cleaned_data['price']
            lab_instance = form.cleaned_data['lab_name']
            form_data = form.cleaned_data
            form_data['lab_name'] = lab_instance.lab_name if lab_instance else None

            try:
                doctor = Doctors.objects.get(id=exoo.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (Doctors.DoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab')

            if price_lab is not None:
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price
            else:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            exoo.doctor_share = doctor_share.quantize(Decimal('0.01'))
            exoo.center_share = center_share.quantize(Decimal('0.01'))
            exoo.total_price = total_price.quantize(Decimal('0.01'))
            form.save()

            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(periodontology_instance=exoo, image=photo)

            return redirect('periodontology', id=exoo.idReception1_id)
    else:
        form = PeriodontologyForm(instance=exoo)
        try:
            exoo = Periodontology.objects.get(idReception1=id)
            photos = exoo.photo_set.all()
            if exoo.type:
                exoo.type = exoo.type.replace("'", "")
        except Periodontology.DoesNotExist:
            exoo = None
            photos = None

    labs = Lab.objects.all()  # Get all labs
    return render(request, 'periodontology/periodontology_edit.html',
                  {'form': form, 'id': id, 'exoo': exoo, 'labs': labs, 'photos': photos})


def periodontology_reception(request):
    appointments =Reception1.objects.all().order_by('-id')
    p = Paginator(appointments, 25)  # Paginator
    page = request.GET.get('page')  # Paginator
    appointments = p.get_page(page)  # Paginator
    nums = "a" * appointments.paginator.num_pages  # Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'periodontology/periodontology_reception.html', {'appointments': appointments})


def add_linebreaks(values, n):
    value_list = values.split(', ')
    new_values = [',  '.join(value_list[i:i+n]) for i in range(0, len(value_list), n)]
    for i in range(1, len(new_values)):
        new_values[i] = '- ' + new_values[i]
    return '<br>'.join(new_values)


def all_exo(request):
    appointments =Exo.objects.all().order_by('-id')

    for appointment in appointments:
        appointment.ur = appointment.ur.replace("'", "")
        appointment.ul = appointment.ul.replace("'", "")
        appointment.lr = appointment.lr.replace("'", "")
        appointment.ll = appointment.ll.replace("'", "")
        appointment.exoby = appointment.exoby.replace("'", "")
        appointment.uper = appointment.uper.replace("'", "")
        appointment.complcated = appointment.complcated.replace("'", "")
    return render(request, 'exo/all_exo.html', {'appointments': appointments})


def send_appointment_reminders(request):
    # Replace with your actual Twilio credentials
    account_sid = 'AC4fc2552605eaf126991299f892900b66'
    auth_token = 'e06e125722056090b1d11783a73e2c4f'

    # Initialize the Twilio client
    client = Client(account_sid, auth_token)

    # Define the criteria for upcoming appointments (e.g., within the next 24 hours)
    # You may need to adjust this based on your application's requirements
    appointments = Reception.objects.all()

    # Iterate over the patients with upcoming appointments
    for appointment in appointments:
        print(appointments)

        message_body = f'Hi {appointment.name}, your appointment is scheduled for {appointment.app_data}, at {appointment.time}.'

        # Send the WhatsApp message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=f'whatsapp:+964{appointment.phone}' # Use the phone field to get the WhatsApp number
        )

        # Handle the response (printing the SID in this example)
        print(message.sid)

    # Return a response to the client (you can customize this as needed)
    return JsonResponse({'status': 'Appointment reminders sent successfully'})


def medicine(request, id):
    if request.method == 'POST':
        form = MedicinForm(request.POST)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name
            oral_surgery.phone = reception.phone
            oral_surgery.gender = reception.gender
            oral_surgery.date_of_birth = reception.date_of_birth
            oral_surgery.save()

            return redirect('medicine', id=id)
    else:
        reception = get_object_or_404(Reception, id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = MedicinForm(initial=initial_data)

    appointments = Reception.objects.all().order_by('-id')
    try:
        medicine = Medicin.objects.filter(idReception=id).first()
    except Medicin.DoesNotExist:
        medicine = None
        # Replace commas in Exo model fields
    if medicine:
        medicine.antibiotic = medicine.antibiotic.replace("'", "")
        medicine.analogous = medicine.analogous.replace("'", "")
        medicine.mouthwash = medicine.mouthwash.replace("'", "")
        # Add line breaks for specific fields
        medicine.antibiotic = add_linebreaks(medicine.antibiotic, 4)
        medicine.analogous = add_linebreaks(medicine.analogous, 4)
        medicine.mouthwash = add_linebreaks(medicine.mouthwash, 4)

    return render(request, 'exo/medicine.html',
                  {'form': form, 'appointments': appointments, 'medicine': medicine, 'id': id})


def all_medicine(request):
    appointments = Medicin.objects.all().order_by('-id')

    for appointment in appointments:
        appointment.antibiotic = appointment.antibiotic.replace("'", "")
        appointment.analogous = appointment.analogous.replace("'", "")
        appointment.mouthwash = appointment.mouthwash.replace("'", "")
        # Add line breaks for specific fields
        appointment.antibiotic = add_linebreaks(appointment.antibiotic, 4)
        appointment.analogous = add_linebreaks(appointment.analogous, 4)
        appointment.mouthwash = add_linebreaks(appointment.mouthwash, 4)

    return render(request, 'exo/all_medicine.html', {'appointments': appointments})


def print_medicine(request, id):
    appointment = get_object_or_404(Medicin, id=id)
    # Modify appointment fields
    appointment.antibiotic = appointment.antibiotic.replace("'", "")
    appointment.analogous = appointment.analogous.replace("'", "")
    appointment.mouthwash = appointment.mouthwash.replace("'", "")
    # Add line breaks for specific fields
    appointment.antibiotic = add_linebreaks(appointment.antibiotic, 4)
    appointment.analogous = add_linebreaks(appointment.analogous, 4)
    appointment.mouthwash = add_linebreaks(appointment.mouthwash, 4)

    # Pass the appointment data to the template
    context = {
        'appointment': appointment,
    }

    return render(request, 'exo/print_medicine.html', context)


def print_medicine1(request, id):
    appointment = get_object_or_404(Medicin, id=id)
    # Modify appointment fields
    appointment.antibiotic = appointment.antibiotic.replace("'", "")
    appointment.analogous = appointment.analogous.replace("'", "")
    appointment.mouthwash = appointment.mouthwash.replace("'", "")
    # Add line breaks for specific fields
    appointment.antibiotic = add_linebreaks(appointment.antibiotic, 4)
    appointment.analogous = add_linebreaks(appointment.analogous, 4)
    appointment.mouthwash = add_linebreaks(appointment.mouthwash, 4)

    # Pass the appointment data to the template
    context = {
        'appointment': appointment,
    }

    return render(request, 'exo/print_medicine1.html', context)


def search_exo(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'exo/search_exo.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'exo/search_exo.html', {})


def search_prosthodontics(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'prosthodontics/search_prosthodontics.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'prosthodontics/search_prosthodontics.html', {})


def search_exo1(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'exo/search_exo1.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'exo/search_exo1.html', {})


def delete_exo(request, id):
    # Get the drug related to the Reception
    exo = get_object_or_404(Exo, id=id)

    # Store the idReception before deleting the drug
    idReception = exo.idReception1_id

    # Delete the drug
    exo.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('exo', id=idReception)


def drugs(request, id):
    reception = get_object_or_404(Reception1, id=id)

    if request.method == 'POST':
        form = DrugForm(request.POST)
        formset = DrugFormSet(request.POST, prefix='drugs')

        if form.is_valid() and formset.is_valid():
            drugs = form.save(commit=False)
            drugs.idReception_id = reception.idReception_id
            drugs.idReception1_id = id
            drugs.name = reception.name
            drugs.phone = reception.phone
            drugs.gender = reception.gender
            drugs.date_of_birth = reception.date_of_birth
            drugs.save()

            for drug_form in formset:
                if drug_form.cleaned_data.get('name_medicine'):
                    drug = drug_form.save(commit=False)
                    drug.idReception_id = reception.idReception_id
                    drug.idReception1_id = id
                    drug.name = reception.name
                    drug.phone = reception.phone
                    drug.gender = reception.gender
                    drug.date_of_birth = reception.date_of_birth
                    drug.name_medicine = drug_form.cleaned_data['name_medicine'].name_medicine
                    drug.save()

            return redirect('drugs', id=id)
    else:
        initial_data = {
            'idReception': reception.idReception_id,
            'idReception1_id': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = DrugForm(initial=initial_data)
        formset = DrugFormSet(prefix='drugs')

    appointments = Reception1.objects.all().order_by('-id')
    try:
        medicines = Drug.objects.filter(idReception1=id)
    except Drug.DoesNotExist:
        medicines = None

    return render(request, 'drugs/drugs.html', {
        'form': form,
        'formset': formset,
        'appointments': appointments,
        'medicines': medicines,
        'id': id
    })


def delete_drugs(request, id):
    # Get the drug related to the Reception
    drug = get_object_or_404(Drug, id=id)

    # Store the idReception before deleting the drug
    idReception = drug.idReception1_id

    # Delete the drug
    drug.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('drugs', id=idReception)


def print_drugs(request, id):
    drugs = Drug.objects.filter(idReception1=id)
    context = {
        'drugs': drugs,
    }
    return render(request, 'drugs/print_drugs.html', context)


def crown_reception(request):
    appointments =Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,25) #Paginator
    page = request.GET.get('page') #Paginator
    appointments = p.get_page(page)#Paginator
    nums = "a" * appointments.paginator.num_pages#Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/crown/crown_reception.html', {'appointments': appointments})


def search_crown(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'conservation/crown/search_crown.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/crown/search_crown.html', {})


@login_required
def crown(request, id):
    user = request.user

    try:
        # Check if the user is an admin or the doctor associated with the reception
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            doctor = Doctors.objects.get(user=user)
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = CrownForm(request.POST, request.FILES)
            if form.is_valid():
                crown_instance = form.save(commit=False)
                crown_instance.idReception1_id = id

                # Set additional fields from reception
                crown_instance.idReception_id = reception.idReception_id
                crown_instance.name = reception.name
                crown_instance.phone = reception.phone
                crown_instance.gender = reception.gender
                crown_instance.date_of_birth = reception.date_of_birth
                crown_instance.educational_id = reception.educational_id
                crown_instance.doctor_id = reception.doctor_id

                # Calculate total price and shares
                price = form.cleaned_data['price']
                price = Decimal(price)  # Convert price to Decimal

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                crown_instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
                crown_instance.center_share = center_share.quantize(Decimal('0.01'))
                crown_instance.total_price = total_price.quantize(Decimal('0.01'))
                crown_instance.price_lab = price_lab_decimal  # Save price_lab as Decimal

                crown_instance.save()

                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(crown_instance=crown_instance, image=photo)

                return redirect('crown', id=id)

        else:
            initial_data = {
                'idReception1_id': id,
                'idReception_id': reception.idReception_id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'doctor_id': reception.doctor_id
            }
            form = CrownForm(initial=initial_data)

    except (ObjectDoesNotExist, Doctors.DoesNotExist):
        messages.error(request, 'Reception does not exist or you do not have permission to access it.')
        return redirect('home')

    appointments = Reception1.objects.all().order_by('-id')
    crownn = Crown.objects.filter(idReception1=id)
    photos_list = [crown.photo_set.all() for crown in crownn]

    try:
        crown = crownn.first()
        photos = crown.photo_set.all()
    except AttributeError:
        crown = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None

    formatted_total_prices = ["{:,.2f}".format(crown.total_price) if crown.total_price is not None else None for crown in crownn]
    formatted_prices = ["{:,.2f}".format(crown.price) if crown.price is not None else None for crown in crownn]

    return render(request, 'conservation/crown/crown.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'crownn': crownn,
        'id': id,
        'photos': photos,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


def crown_edit(request, id):
    pi = Crown.objects.get(id=id)
    photos = Photo.objects.filter(crown_instance=pi)  # Fetch photos associated with the exo instance

    if request.method == 'POST':
        form = CrownForm(request.POST, instance=pi)
        if form.is_valid():
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']

            try:
                doctor = Doctors.objects.get(id=pi.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            pi.doctor_share = doctor_share.quantize(Decimal('0.01'))
            pi.center_share = center_share.quantize(Decimal('0.01'))
            pi.total_price = total_price.quantize(Decimal('0.01'))
            # Handle lab_name separately
            selected_lab = form.cleaned_data['lab_name']
            if selected_lab:
                pi.lab = selected_lab  # Set the foreign key to the selected Lab
                pi.lab_name = selected_lab.lab_name  # Save the lab_name as well
            pi.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(crown_instance=pi, image=photo)

            return redirect('crown', id=pi.idReception1_id)
    else:
        form = CrownForm(instance=pi)
    labs = Lab.objects.all()
    return render(request, 'conservation/crown/crown_edit.html', {'form': form, 'pi': pi, 'photos': photos, 'labs': labs})


def remove_photo_crown(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    crown_instance = photo.crown_instance
    photo.delete()
    return redirect('crown_edit', id=crown_instance.id)


def delete_crown(request, id):
    # Get the drug related to the Reception
    crown = get_object_or_404(Crown, id=id)

    # Store the idReception before deleting the drug
    idReception = crown.idReception1_id

    # Delete the drug
    crown.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('crown', id=idReception)


def veneer_reception(request):
    appointments =Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,20) #Paginator
    page = request.GET.get('page') #Paginator
    appointments = p.get_page(page)#Paginator
    nums = "a" * appointments.paginator.num_pages#Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/veneer/veneer_reception.html', {'appointments': appointments})


def search_veneer(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'conservation/veneer/search_veneer.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/veneer/search_veneer.html', {})


@login_required
def veneer(request, id):
    try:
        user = request.user

        # Check if the user is an admin or the doctor associated with the reception
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            doctor = Doctors.objects.get(user=user)
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = VeneerForm(request.POST, request.FILES)
            if form.is_valid():
                veneer_instance = form.save(commit=False)
                veneer_instance.idReception1_id = id

                # Set additional fields from reception
                veneer_instance.idReception_id = reception.idReception_id
                veneer_instance.name = reception.name
                veneer_instance.phone = reception.phone
                veneer_instance.gender = reception.gender
                veneer_instance.date_of_birth = reception.date_of_birth
                veneer_instance.educational_id = reception.educational_id
                veneer_instance.doctor_id = reception.doctor_id

                # Calculate total price and shares
                price = form.cleaned_data['price']
                price = Decimal(price)  # Convert price to Decimal


                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                veneer_instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
                veneer_instance.center_share = center_share.quantize(Decimal('0.01'))
                veneer_instance.total_price = total_price.quantize(Decimal('0.01'))
                veneer_instance.price_lab = price_lab_decimal  # Save price_lab as Decimal

                veneer_instance.save()

                # Save associated photos
                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(veneer_instance=veneer_instance, image=photo)

                return redirect('veneer', id=id)

        else:
            # GET request: Initialize form with initial data
            initial_data = {
                'idReception1_id': id,
                'idReception_id': reception.idReception_id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'doctor_id': reception.doctor_id
            }
            form = VeneerForm(initial=initial_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('home')

    # Fetch necessary data for rendering the template
    appointments = Reception1.objects.all().order_by('-id')
    veneerr = Veneer.objects.filter(idReception1=id)
    photos_list = [veneer.photo_set.all() for veneer in veneerr]

    try:
        veneer = veneerr.first()
        photos = veneer.photo_set.all()
    except AttributeError:
        veneer = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None

    formatted_total_prices = ["{:,.2f}".format(veneer.total_price) if veneer.total_price is not None else None for veneer in veneerr]
    formatted_prices = ["{:,.2f}".format(veneer.price) if veneer.price is not None else None for veneer in veneerr]

    return render(request, 'conservation/veneer/veneer.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'veneerr': veneerr,
        'id': id,
        'photos': photos,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


def veneer_edit(request, id):
    pi = Veneer.objects.get(id=id)
    photos = Photo.objects.filter(veneer_instance=pi)  # Fetch photos associated with the exo instance

    if request.method == 'POST':
        form = VeneerForm(request.POST, instance=pi)
        if form.is_valid():
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']

            try:
                doctor = Doctors.objects.get(id=pi.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            # Assign Decimal values to model fields
            form.instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
            form.instance.center_share = center_share.quantize(Decimal('0.01'))
            form.instance.total_price = total_price.quantize(Decimal('0.01'))
            form.instance.price_lab = price_lab_decimal  # Save price_lab as Decimal
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(veneer_instance=pi, image=photo)

            return redirect('veneer', id=pi.idReception1_id)
    else:
        form = VeneerForm(instance=pi)
    labs = Lab.objects.all()
    return render(request, 'conservation/veneer/veneer_edit.html', {'form': form, 'pi': pi, 'photos': photos, 'labs': labs})


def delete_veneer(request, id):
    # Get the drug related to the Reception
    veneer = get_object_or_404(Veneer, id=id)

    # Store the idReception before deleting the drug
    idReception = veneer.idReception1_id

    # Delete the drug
    veneer.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('veneer', id=idReception)


def remove_photo_veneer(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    veneer_instance = photo.veneer_instance
    photo.delete()
    return redirect('veneer_edit', id=veneer_instance.id)


@login_required
def filling(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)
    except Doctors.DoesNotExist:
        # Handle the case where the doctor does not exist
        return redirect('error_page')  # Redirect to an error page or handle appropriately

    if request.method == 'POST':
        form = FillingForm(request.POST, request.FILES)
        if form.is_valid():
            filling_instance = form.save(commit=False)
            filling_instance.idReception1_id = id
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']
            filling_instance.idReception_id = reception.idReception_id
            filling_instance.name = reception.name
            filling_instance.phone = reception.phone
            filling_instance.gender = reception.gender
            filling_instance.date_of_birth = reception.date_of_birth
            filling_instance.educational_id = reception.educational_id
            filling_instance.doctor_id = reception.doctor_id

            try:
                doctor = Doctors.objects.get(id=reception.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            # Assign Decimal values to model fields
            filling_instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
            filling_instance.center_share = center_share.quantize(Decimal('0.01'))
            filling_instance.total_price = total_price.quantize(Decimal('0.01'))
            filling_instance.price_lab = price_lab_decimal  # Save price_lab as Decimal
            filling_instance.save()

            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(filling_instance=filling_instance, image=photo)

            return redirect('filling', id=id)
    else:
        initial_data = {
            'idReception1_id': id,
            'idReception_id': reception.idReception_id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth,
            'educational_id': reception.educational_id,
            'doctor_id': reception.doctor_id
        }
        form = FillingForm(initial=initial_data)

    appointments = Reception1.objects.all().order_by('-id')
    fillingg = Filling.objects.filter(idReception1=id)
    photos_list = []

    try:
        filling = fillingg.first()
        photos = filling.photo_set.all()
    except AttributeError:
        filling = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None

    for fill in fillingg:
        if fill.filling_type:
            fill.filling_type = fill.filling_type.replace("'", "")
        if fill.ur:
            fill.ur = fill.ur.replace("'", "")
        if fill.ul:
            fill.ul = fill.ul.replace("'", "")
        if fill.lr:
            fill.lr = fill.lr.replace("'", "")
        if fill.ll:
            fill.ll = fill.ll.replace("'", "")

        photos = fill.photo_set.all()
        photos_list.append(photos)

    formatted_total_prices = ["{:,.2f}".format(fill.total_price) if fill.total_price is not None else None for fill in fillingg]
    formatted_prices = ["{:,.2f}".format(fill.price) if fill.price is not None else None for fill in fillingg]

    return render(request, 'conservation/filling/filling.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'fillingg': fillingg,
        'id': id,
        'photos': photos,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


@login_required
def pedo(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = PedoForm(request.POST, request.FILES)
            if form.is_valid():
                pedo_instance = form.save(commit=False)
                pedo_instance.idReception1_id = id

                price = form.cleaned_data['price']
                price = Decimal(price)  # Convert price to Decimal
                pedo_instance.price = price
                pedo_instance.name = reception.name
                pedo_instance.phone = reception.phone
                pedo_instance.gender = reception.gender
                pedo_instance.date_of_birth = reception.date_of_birth
                pedo_instance.educational_id = reception.educational_id
                pedo_instance.idReception_id = reception.idReception_id
                pedo_instance.doctor_id = reception.doctor_id

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                pedo_instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
                pedo_instance.center_share = center_share.quantize(Decimal('0.01'))
                pedo_instance.price_lab = price_lab_decimal  # Save price_lab as Decimal
                pedo_instance.total_price = total_price.quantize(Decimal('0.01'))

                pedo_instance.save()

                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(pedo_instance=pedo_instance, image=photo)

                return redirect('pedo', id=id)
        else:
            form = PedoForm(initial={
                'idReception1_id': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'idReception_id': reception.idReception_id,
                'doctor_id': reception.doctor_id
            })

        appointments = Reception1.objects.all().order_by('-id')
        fillingg = Pedo.objects.filter(idReception1=id)
        photos_list = []

        try:
            filling = fillingg.first()
            photos = filling.photo_set.all()
        except AttributeError:
            filling = None
            photos = None

        try:
            medicine = Medicin.objects.get(idReception=id)
        except Medicin.DoesNotExist:
            medicine = None

        for fill in fillingg:
            if fill.filling_type:
                fill.filling_type = fill.filling_type.replace("'", "")
            if fill.ur:
                fill.ur = fill.ur.replace("'", "")
            if fill.ul:
                fill.ul = fill.ul.replace("'", "")
            if fill.lr:
                fill.lr = fill.lr.replace("'", "")
            if fill.ll:
                fill.ll = fill.ll.replace("'", "")

            photos = fill.photo_set.all()
            photos_list.append(photos)

        formatted_total_prices = ["{:,.2f}".format(fill.total_price) if fill.total_price is not None else None for fill in fillingg]
        formatted_prices = ["{:,.2f}".format(fill.price) if fill.price is not None else None for fill in fillingg]

        return render(request, 'conservation/pedo/pedo.html', {
            'form': form,
            'appointments': appointments,
            'medicine': medicine,
            'fillingg': fillingg,
            'id': id,
            'photos': photos,
            'photos_list': photos_list,
            'formatted_total_prices': formatted_total_prices,
            'formatted_prices': formatted_prices
        })
    except Doctors.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    except Reception1.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'Reception does not exist or you do not have permission to access it.')
        return redirect('home')


def filling_reception(request):
    appointments =Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,20) #Paginator
    page = request.GET.get('page') #Paginator
    appointments = p.get_page(page)#Paginator
    nums = "a" * appointments.paginator.num_pages#Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/filling/filling_reception.html', {'appointments': appointments})


def pedo_reception(request):
    appointments =Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,20) #Paginator
    page = request.GET.get('page') #Paginator
    appointments = p.get_page(page)#Paginator
    nums = "a" * appointments.paginator.num_pages#Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/pedo/pedo_reception.html', {'appointments': appointments})


def search_pedo(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'conservation/pedo/search_pedo.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/filling/search_filling.html', {})

def search_filling(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'conservation/filling/search_filling.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/filling/search_filling.html', {})


def filling_edit(request, id):
    pi = Filling.objects.get(id=id)
    photos = Photo.objects.filter(filling_instance=pi)  # Fetch photos associated with the exo instance

    if request.method == 'POST':
        form = FillingForm(request.POST, instance=pi)
        if form.is_valid():
            price = form.cleaned_data['price']

            try:
                doctor = Doctors.objects.get(id=pi.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            # Assign Decimal values to model fields
            form.instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
            form.instance.center_share = center_share.quantize(Decimal('0.01'))
            form.instance.total_price = total_price.quantize(Decimal('0.01'))
            form.instance.price_lab = price_lab_decimal  # Save price_lab as Decimal
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(filling_instance=pi, image=photo)

            return redirect('filling', id=pi.idReception1_id)
    else:
        form = FillingForm(instance=pi)
    labs = Lab.objects.all()
    return render(request, 'conservation/filling/filling_edit.html', {'form': form, 'pi': pi, 'photos': photos, 'labs': labs})


def pedo_edit(request, id):
    pi = Pedo.objects.get(id=id)
    photos = Photo.objects.filter(pedo_instance=pi)  # Fetch photos associated with the pedo instance

    if request.method == 'POST':
        form = PedoForm(request.POST, instance=pi)
        if form.is_valid():
            price = form.cleaned_data['price']

            try:
                doctor = Doctors.objects.get(id=pi.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            # Assign Decimal values to model fields
            form.instance.doctor_share = doctor_share.quantize(Decimal('0.01'))
            form.instance.center_share = center_share.quantize(Decimal('0.01'))
            form.instance.price_lab = price_lab_decimal  # Save price_lab as Decimal
            form.instance.total_price = total_price.quantize(Decimal('0.01'))
            form.save()

            # Update associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(pedo_instance=pi, image=photo)

            return redirect('pedo', id=pi.idReception1_id)
    else:
        form = PedoForm(instance=pi)

    appointments = Reception1.objects.all().order_by('-id')
    fillingg = Pedo.objects.filter(idReception1=pi.idReception1_id)
    photos_list = []

    try:
        filling = fillingg.first()
        photos = filling.photo_set.all()
    except AttributeError:
        filling = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=pi.idReception1_id)
    except Medicin.DoesNotExist:
        medicine = None

    for fill in fillingg:
        if fill.filling_type:
            fill.filling_type = fill.filling_type.replace("'", "")
        if fill.ur:
            fill.ur = fill.ur.replace("'", "")
        if fill.ul:
            fill.ul = fill.ul.replace("'", "")
        if fill.lr:
            fill.lr = fill.lr.replace("'", "")
        if fill.ll:
            fill.ll = fill.ll.replace("'", "")

        photos = fill.photo_set.all()
        photos_list.append(photos)

    formatted_total_prices = ["{:,.2f}".format(fill.total_price) if fill.total_price is not None else None for fill in fillingg]
    formatted_prices = ["{:,.2f}".format(fill.price) if fill.price is not None else None for fill in fillingg]
    labs = Lab.objects.all()
    return render(request, 'conservation/pedo/pedo_edit.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'fillingg': fillingg,
        'id': id,
        'photos': photos,
        'labs': labs,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


def delete_pedo(request, id):
    # Get the drug related to the Reception
    filling = get_object_or_404(Pedo, id=id)

    # Store the idReception before deleting the drug
    idReception = filling.idReception1_id

    # Delete the drug
    filling.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('pedo', id=idReception)


def delete_filling(request, id):
    # Get the drug related to the Reception
    filling = get_object_or_404(Filling, id=id)

    # Store the idReception before deleting the drug
    idReception = filling.idReception1_id

    # Delete the drug
    filling.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('filling', id=idReception)


def remove_photo_filling(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    filling_instance = photo.filling_instance
    photo.delete()
    return redirect('filling_edit', id=filling_instance.id)


def remove_photo_pedo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    pedo_instance = photo.pedo_instance
    photo.delete()
    return redirect('pedo_edit', id=pedo_instance.id)


def add_debt(request, id):
    try:
        exo_instance = Exo.objects.get(id=id)
    except Exo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(exo_instance=exo_instance)
    previous_date = exo_instance.date
    previous_paid = exo_instance.paid
    total_price = exo_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if exo_instance.paid + paid >= total_price:
            exo_instance.paid = total_price
        else:
            exo_instance.paid += paid  # Increment the paid amount

        exo_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(exo_instance=exo_instance, previous_date=date, paid_amount=paid,
                                         idReception1=exo_instance.idReception1, idReception=exo_instance.idReception, name=exo_instance.name, phone=exo_instance.phone, price=exo_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt.html', {
            'id': id,
            'exo_instance': exo_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt1(request, id):
    try:
        exo_instance = Exo.objects.get(id=id)
    except Exo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(exo_instance=exo_instance)
    previous_date = exo_instance.date
    previous_paid = exo_instance.paid
    total_price = exo_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if exo_instance.paid + paid >= total_price:
            exo_instance.paid = total_price
        else:
            exo_instance.paid += paid  # Increment the paid amount

        exo_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(exo_instance=exo_instance, previous_date=date, paid_amount=paid,
                                         idReception=exo_instance.idReception, idReception1=exo_instance.idReception1, name=exo_instance.name,
                                         phone=exo_instance.phone, price=exo_instance.total_price)
        payment_history.save()

        return redirect(reverse(
            'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt.html', {
            'id': id,
            'exo_instance': exo_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def print_exo_debt(request, id):
    debts = PaymentHistory.objects.filter(idReception1=id).values('id', 'previous_date', 'paid_amount', 'name', 'phone')
    debt1 = Exo.objects.filter(idReception1=id).values_list('id', 'paid', 'total_price', 'name', 'phone')
    debt2 = Crown.objects.filter(idReception1=id).values_list('id', 'paid', 'total_price', 'name', 'phone')
    debt3 = Filling.objects.filter(idReception1=id).values_list('id', 'paid',  'total_price', 'name', 'phone')
    debt4 = Endo.objects.filter(idReception1=id).values_list('id', 'paid',  'total_price', 'name', 'phone')
    debt5 = Ortho.objects.filter(idReception1=id, visits_id__isnull=True).values_list('id', 'paid', 'total_price', 'name', 'phone')
    debt6 = OralSurgery.objects.filter(idReception1=id).values_list('id', 'paid',  'total_price', 'name', 'phone')
    debt7 = Prosthodontics.objects.filter(idReception1=id).values_list('id', 'paid',  'total_price', 'name', 'phone')
    debt8 = Periodontology.objects.filter(idReception1=id).values_list('id', 'paid', 'total_price', 'name', 'phone')
    debt9 = Veneer.objects.filter(idReception1=id).values_list('id', 'paid',  'total_price', 'name', 'phone')
    debt10 = Pedo.objects.filter(idReception1=id).values_list('id', 'paid',  'total_price', 'name', 'phone')
    debt11 = Surgery.objects.filter(idReception1=id).values_list('id', 'paid', 'total_price', 'name', 'phone')
    debt12 = Preventive.objects.filter(idReception1=id).values_list('id', 'paid', 'total_price', 'name', 'phone')
    combined_debts = debts.union(debt1, debt2, debt3, debt4, debt5, debt6, debt7, debt8, debt9,debt10,debt11,debt12)
    debtss = PaymentHistory.objects.filter(idReception1=id).values('id', 'previous_date', 'paid_amount', 'name', 'phone')

    # Calculate the total remaining amount for idReception
    total_exo = Exo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_filling = Filling.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_pedo = Pedo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_crown = Crown.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_endo = Endo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_ortho = Ortho.objects.filter(idReception1=id, visits_id__isnull=True).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_surgery = Surgery.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_preventive = Preventive.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    paid_exo = Exo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_filling = Filling.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_pedo = Pedo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_crown = Crown.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_endo = Endo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_ortho = Ortho.objects.filter(idReception1=id, visits_id__isnull=True).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_surgery = Surgery.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0
    paid_preventive = Preventive.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    total_price = (total_exo + total_filling + total_crown + total_veneer + total_oralSurgery + total_endo + total_ortho + total_periodontology + total_prosthodontics + total_pedo+ total_surgery+ total_preventive)
    total_paid = (paid_exo + paid_filling + paid_crown + paid_veneer + paid_oralSurgery + paid_endo + paid_ortho + paid_periodontology + paid_prosthodontics+ paid_pedo + paid_surgery+ paid_preventive)
    total_remaining = total_price - total_paid

    context = {

        'debts': debts,
        'debt1': debt1,
        'debt2': debt2,
        'debt3': debt3,
        'debt4': debt4,
        'debt5': debt5,
        'debt6': debt6,
        'debt7': debt7,
        'debt8': debt8,
        'debt9': debt9,
        'debt10': debt10,
        'debt11': debt11,
        'debt12': debt12,
        'debtss': debtss,
        'combined_debts': combined_debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'total_exo': total_exo,  # Add total_salary to the context
        'total_filling': total_filling,  # Add total_salary to the context
        'total_pedo': total_filling,  # Add total_salary to the context
        'total_crown': total_crown,  # Add total_salary to the context
        'total_veneer': total_veneer,  # Add total_salary to the context
        'total_oralSurgery': total_oralSurgery,  # Add total_salary to the context
        'total_endo': total_endo,  # Add total_salary to the context
        'total_ortho': total_ortho,  # Add total_salary to the context
        'total_periodontology': total_periodontology,  # Add total_salary to the context
        'total_prosthodontics': total_prosthodontics,  # Add total_salary to the context
        'total_surgery': total_surgery,  # Add total_salary to the context
        'total_preventive': total_preventive,  # Add total_salary to the context
        'paid_exo': paid_exo,  # Add total_salary to the context
        'paid_filling': paid_filling,  # Add total_salary to the context
        'paid_pedo': paid_filling,  # Add total_salary to the context
        'paid_crown': paid_crown,  # Add paid_salary to the context
        'paid_veneer': paid_veneer,  # Add paid_salary to the context
        'paid_oralSurgery': paid_oralSurgery,  # Add paid_salary to the context
        'paid_endo': paid_endo,  # Add paid_salary to the context
        'paid_ortho': paid_ortho,  # Add paid_salary to the context
        'paid_periodontology': paid_periodontology,  # Add paid_salary to the context
        'paid_prosthodontics': paid_prosthodontics,  # Add paid_salary to the context
        'paid_surgery': paid_surgery,
        'paid_preventive': paid_preventive,
    }
    return render(request, 'debts/print_exo_debt.html', context)


def add_debt_crown(request, id):
    try:
        crown_instance = Crown.objects.get(id=id)
    except Crown.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(crown_instance=crown_instance)
    previous_date = crown_instance.date
    previous_paid = crown_instance.paid
    total_price = crown_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if crown_instance.paid + paid >= total_price:
            crown_instance.paid = total_price
        else:
            crown_instance.paid += paid  # Increment the paid amount

        crown_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(crown_instance=crown_instance, previous_date=date, paid_amount=paid,
                                         idReception1=crown_instance.idReception1, idReception=crown_instance.idReception, name=crown_instance.name, phone=crown_instance.phone, price=crown_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_crown.html', {
            'id': id,
            'crown_instance': crown_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_crown1(request, id):
    try:
        crown_instance = Crown.objects.get(id=id)
    except Crown.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(crown_instance=crown_instance)
    previous_date = crown_instance.date
    previous_paid = crown_instance.paid
    total_price = crown_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if crown_instance.paid + paid >= total_price:
                crown_instance.paid = total_price
            else:
                crown_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            crown_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                crown_instance=crown_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=crown_instance.idReception,
                idReception1=crown_instance.idReception1,
                name=crown_instance.name,
                phone=crown_instance.phone,
                price=crown_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_crown.html', {
        'id': id,
        'crown_instance': crown_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })


def print_crown_debt(request, id):
    debts = PaymentHistory.objects.filter(idReception1=id)

    # Calculate the total remaining amount for idReception
    total_exo = Exo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_filling = Filling.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_crown = Crown.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_endo = Endo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_ortho = Ortho.objects.filter(idReception1=id).aggregate(total_price=Sum('price'))['total_price'] or 0

    total_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    paid_exo = Exo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_filling = Filling.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_crown = Crown.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_endo = Endo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_ortho = Ortho.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    total_price = (total_exo + total_filling + total_crown + total_veneer + total_oralSurgery + total_endo + total_ortho + total_periodontology + total_prosthodontics)
    total_paid = (paid_exo + paid_filling + paid_crown + paid_veneer + paid_oralSurgery + paid_endo + paid_ortho + paid_periodontology + paid_prosthodontics)
    total_remaining = total_price - total_paid



    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_exo': total_exo,  # Add total_salary to the context
        'total_filling': total_filling,  # Add total_salary to the context
        'total_crown': total_crown,  # Add total_salary to the context
        'total_veneer': total_veneer,  # Add total_salary to the context
        'total_oralSurgery': total_oralSurgery,  # Add total_salary to the context
        'total_endo': total_endo,  # Add total_salary to the context
        'total_ortho': total_ortho,  # Add total_salary to the context
        'total_periodontology': total_periodontology,  # Add total_salary to the context
        'total_prosthodontics': total_prosthodontics,  # Add total_salary to the context
        'paid_exo': paid_exo,  # Add total_salary to the context
        'paid_filling': paid_filling,  # Add total_salary to the context
        'paid_crown': paid_crown,  # Add paid_salary to the context
        'paid_veneer': paid_veneer,  # Add paid_salary to the context
        'paid_oralSurgery': paid_oralSurgery,  # Add paid_salary to the context
        'paid_endo': paid_endo,  # Add paid_salary to the context
        'paid_ortho': paid_ortho,  # Add paid_salary to the context
        'paid_periodontology': paid_periodontology,  # Add paid_salary to the context
        'paid_prosthodontics': paid_prosthodontics,  # Add paid_salary to the context

    }

    return render(request, 'debts/print_crown_debt.html', context)


def add_debt_ortho(request, id):
    try:
        ortho_instance = Ortho.objects.get(id=id)
    except Ortho.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(ortho_instance=ortho_instance)
    previous_date = ortho_instance.date
    previous_paid = ortho_instance.paid
    total_price = ortho_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if ortho_instance.paid + paid >= total_price:
            ortho_instance.paid = total_price
        else:
            ortho_instance.paid += paid  # Increment the paid amount

        ortho_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(ortho_instance=ortho_instance, previous_date=date, paid_amount=paid,
                                         idReception1=ortho_instance.idReception1, idReception=ortho_instance.idReception, name=ortho_instance.name,
                                         phone=ortho_instance.phone, price=ortho_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_ortho.html', {
            'id': id,
            'ortho_instance': ortho_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_ortho1(request, id):
    try:
        ortho_instance = Ortho.objects.get(id=id)
    except Ortho.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(ortho_instance=ortho_instance)
    previous_date = ortho_instance.date
    previous_paid = ortho_instance.paid
    total_price = ortho_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if ortho_instance.paid + paid >= total_price:
                ortho_instance.paid = total_price
            else:
                ortho_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            ortho_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                ortho_instance=ortho_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=ortho_instance.idReception,
                idReception1=ortho_instance.idReception1,
                name=ortho_instance.name,
                phone=ortho_instance.phone,
                price=ortho_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_ortho.html', {
        'id': id,
        'ortho_instance': ortho_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })


def print_ortho_debt(request, id):
    try:
        ortho_instance = Ortho.objects.get(id=id)
    except Ortho.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(ortho_instance=ortho_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = ortho_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_paid': total_paid,
        'total_price': total_price,
        'patient_name': ortho_instance.name,
        'patient_phone': ortho_instance.phone,
    }

    return render(request, 'debts/print_ortho_debt.html', context)


def add_debt_filling(request, id):
    try:
        filling_instance = Filling.objects.get(id=id)
    except Filling.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(filling_instance=filling_instance)
    previous_date = filling_instance.date
    previous_paid = filling_instance.paid
    total_price = filling_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if filling_instance.paid + paid >= total_price:
            filling_instance.paid = total_price
        else:
            filling_instance.paid += paid  # Increment the paid amount

        filling_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(filling_instance=filling_instance, previous_date=date, paid_amount=paid,
                                         idReception1=filling_instance.idReception1, idReception=filling_instance.idReception, name=filling_instance.name,
                                         phone=filling_instance.phone, price=filling_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_filling.html', {
            'id': id,
            'filling_instance': filling_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_pedo(request, id):
    try:
        pedo_instance = Pedo.objects.get(id=id)
    except Pedo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(pedo_instance=pedo_instance)
    previous_date = pedo_instance.date
    previous_paid = pedo_instance.paid
    total_price = pedo_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if pedo_instance.paid + paid >= total_price:
            pedo_instance.paid = total_price
        else:
            pedo_instance.paid += paid  # Increment the paid amount

        pedo_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(pedo_instance=pedo_instance, previous_date=date, paid_amount=paid,
                                         idReception1=pedo_instance.idReception1, idReception=pedo_instance.idReception, name=pedo_instance.name,
                                         phone=pedo_instance.phone, price=pedo_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_pedo.html', {
            'id': id,
            'pedo_instance': pedo_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_filling1(request, id):
    try:
        filling_instance = Filling.objects.get(id=id)
    except Filling.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(filling_instance=filling_instance)
    previous_date = filling_instance.date
    previous_paid = filling_instance.paid
    total_price = filling_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if filling_instance.paid + paid >= total_price:
                filling_instance.paid = total_price
            else:
                filling_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            filling_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                filling_instance=filling_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=filling_instance.idReception,
                idReception1=filling_instance.idReception1,
                name=filling_instance.name,
                phone=filling_instance.phone,
                price=filling_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_filling.html', {
        'id': id,
        'filling_instance': filling_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })


def print_filling_debt(request, id):
    try:
        filling_instance = Filling.objects.get(id=id)
    except Filling.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(filling_instance=filling_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = filling_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': filling_instance.name,
        'patient_phone': filling_instance.phone,
    }

    return render(request, 'debts/print_filling_debt.html', context)


def print_pedo_debt(request, id):
    try:
        pedo_instance = Pedo.objects.get(id=id)
    except Pedo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(pedo_instance=pedo_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = pedo_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': pedo_instance.name,
        'patient_phone': pedo_instance.phone,
    }

    return render(request, 'debts/print_pedo_debt.html', context)


def print_exo_debt1(request, id):
    try:
        exo_instance = Exo.objects.get(id=id)
    except Exo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(exo_instance=exo_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = exo_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': exo_instance.name,
        'patient_phone': exo_instance.phone,
    }

    return render(request, 'debts/print_exo_debt1.html', context)


def print_crown_debt1(request, id):
    try:
        crown_instance = Crown.objects.get(id=id)
    except Crown.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(crown_instance=crown_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = crown_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': crown_instance.name,
        'patient_phone': crown_instance.phone,
    }

    return render(request, 'debts/print_crown_debt1.html', context)


def add_debt_veneer(request, id):
    try:
        veneer_instance = Veneer.objects.get(id=id)
    except Veneer.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(veneer_instance=veneer_instance)
    previous_date = veneer_instance.date
    previous_paid = veneer_instance.paid
    total_price = veneer_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if veneer_instance.paid + paid >= total_price:
            veneer_instance.paid = total_price
        else:
            veneer_instance.paid += paid  # Increment the paid amount

        veneer_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(veneer_instance=veneer_instance, previous_date=date, paid_amount=paid,
                                         idReception1=veneer_instance.idReception1, idReception=veneer_instance.idReception, name=veneer_instance.name,
                                         phone=veneer_instance.phone, price=veneer_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_veneer.html', {
            'id': id,
            'veneer_instance': veneer_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_veneer1(request, id):
    try:
        veneer_instance = Veneer.objects.get(id=id)
    except Veneer.DoesNotExist:
        return HttpResponse("Endo instance not found")

    previous_dates = PaymentHistory.objects.filter(veneer_instance=veneer_instance)
    previous_date = veneer_instance.date
    previous_paid = veneer_instance.paid
    total_price = veneer_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if veneer_instance.paid + paid >= total_price:
            veneer_instance.paid = total_price
        else:
            veneer_instance.paid += paid  # Increment the paid amount

        veneer_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(veneer_instance=veneer_instance, previous_date=date, paid_amount=paid,
                                         idReception=veneer_instance.idReception,idReception1=veneer_instance.idReception1, name=veneer_instance.name,
                                         phone=veneer_instance.phone, price=veneer_instance.total_price)
        payment_history.save()

        return redirect(reverse(
            'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_veneer.html', {
            'id': id,
            'veneer_instance': veneer_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def print_veneer_debt(request, id):
    try:
        veneer_instance = Veneer.objects.get(id=id)
    except Veneer.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(veneer_instance=veneer_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = veneer_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': veneer_instance.name,
        'patient_phone': veneer_instance.phone,
    }

    return render(request, 'debts/print_veneer_debt.html', context)


def add_debt_periodontology(request, id):
    try:
        periodontology_instance = Periodontology.objects.get(id=id)
    except Periodontology.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(periodontology_instance=periodontology_instance)
    previous_date = periodontology_instance.date
    previous_paid = periodontology_instance.paid
    total_price = periodontology_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if periodontology_instance.paid + paid >= total_price:
            periodontology_instance.paid = total_price
        else:
            periodontology_instance.paid += paid  # Increment the paid amount

        periodontology_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(periodontology_instance=periodontology_instance, previous_date=date, paid_amount=paid,
                                         idReception1=periodontology_instance.idReception1, idReception=periodontology_instance.idReception, name=periodontology_instance.name,
                                         phone=periodontology_instance.phone, price=periodontology_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_periodontology.html', {
            'id': id,
            'periodontology_instance': periodontology_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_periodontology1(request, id):
    try:
        periodontology_instance = Periodontology.objects.get(id=id)
    except Periodontology.DoesNotExist:
        return HttpResponse("Endo instance not found")

    previous_dates = PaymentHistory.objects.filter(periodontology_instance=periodontology_instance)
    previous_date = periodontology_instance.date
    previous_paid = periodontology_instance.paid
    total_price = periodontology_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if periodontology_instance.paid + paid >= total_price:
            periodontology_instance.paid = total_price
        else:
            periodontology_instance.paid += paid  # Increment the paid amount

        periodontology_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(periodontology_instance=periodontology_instance, previous_date=date,
                                         paid_amount=paid,
                                         idReception=periodontology_instance.idReception,
                                         idReception1=periodontology_instance.idReception1,
                                         name=periodontology_instance.name,
                                         phone=periodontology_instance.phone,
                                         price=periodontology_instance.total_price)
        payment_history.save()

        return redirect(reverse(
            'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_periodontology.html', {
            'id': id,
            'periodontology_instance': periodontology_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def print_periodontology_debt(request, id):
    try:
        periodontology_instance = Periodontology.objects.get(id=id)
    except Periodontology.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(periodontology_instance=periodontology_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = periodontology_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': periodontology_instance.name,
        'patient_phone': periodontology_instance.phone,
    }

    return render(request, 'debts/print_periodontology_debt.html', context)


def add_debt_prosthodontics(request, id):
    try:
        prosthodontics_instance = Prosthodontics.objects.get(id=id)
    except Prosthodontics.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(prosthodontics_instance=prosthodontics_instance)
    previous_date = prosthodontics_instance.date
    previous_paid = prosthodontics_instance.paid
    total_price = prosthodontics_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if prosthodontics_instance.paid + paid >= total_price:
            prosthodontics_instance.paid = total_price
        else:
            prosthodontics_instance.paid += paid  # Increment the paid amount

        prosthodontics_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(prosthodontics_instance=prosthodontics_instance, previous_date=date, paid_amount=paid,
                                         idReception1=prosthodontics_instance.idReception1, idReception=prosthodontics_instance.idReception, name=prosthodontics_instance.name,
                                         phone=prosthodontics_instance.phone, price=prosthodontics_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_prosthodontics.html', {
            'id': id,
            'prosthodontics_instance': prosthodontics_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_prosthodontics1(request, id):
    try:
        prosthodontics_instance = Prosthodontics.objects.get(id=id)
    except Prosthodontics.DoesNotExist:
        return HttpResponse("Endo instance not found")

    previous_dates = PaymentHistory.objects.filter(prosthodontics_instance=prosthodontics_instance)
    previous_date = prosthodontics_instance.date
    previous_paid = prosthodontics_instance.paid
    total_price = prosthodontics_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if prosthodontics_instance.paid + paid >= total_price:
            prosthodontics_instance.paid = total_price
        else:
            prosthodontics_instance.paid += paid  # Increment the paid amount

        prosthodontics_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(prosthodontics_instance=prosthodontics_instance, previous_date=date,
                                         paid_amount=paid,
                                         idReception=prosthodontics_instance.idReception,
                                         idReception1=prosthodontics_instance.idReception1,
                                         name=prosthodontics_instance.name,
                                         phone=prosthodontics_instance.phone, price=prosthodontics_instance.total_price)
        payment_history.save()

        return redirect(reverse(
            'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_prosthodontics.html', {
            'id': id,
            'prosthodontics_instance': prosthodontics_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_pedo1(request, id):
    try:
        pedo_instance = Pedo.objects.get(id=id)
    except Pedo.DoesNotExist:
        return HttpResponse("Pedo instance not found")

    previous_dates = PaymentHistory.objects.filter(pedo_instance=pedo_instance)
    previous_date = pedo_instance.date
    previous_paid = pedo_instance.paid
    total_price = pedo_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if pedo_instance.paid + paid >= total_price:
            pedo_instance.paid = total_price
        else:
            pedo_instance.paid += paid  # Increment the paid amount

        pedo_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(pedo_instance=pedo_instance, previous_date=date,
                                         paid_amount=paid,
                                         idReception=pedo_instance.idReception,
                                         idReception1=pedo_instance.idReception1,
                                         name=pedo_instance.name,
                                         phone=pedo_instance.phone, price=pedo_instance.total_price)
        payment_history.save()

        return redirect(reverse(
            'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_pedo.html', {
            'id': id,
            'pedo_instance': pedo_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })



def print_prosthodontics_debt(request, id):
    try:
        prosthodontics_instance = Prosthodontics.objects.get(id=id)
    except Prosthodontics.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(prosthodontics_instance=prosthodontics_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = prosthodontics_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': prosthodontics_instance.name,
        'patient_phone': prosthodontics_instance.phone,
    }

    return render(request, 'debts/print_prosthodontics_debt.html', context)


def add_debt_oral(request, id):
    try:
        oral_surgery_instance = OralSurgery.objects.get(id=id)
    except OralSurgery.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(oral_surgery_instance=oral_surgery_instance)
    previous_date = oral_surgery_instance.date
    previous_paid = oral_surgery_instance.paid
    total_price = oral_surgery_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if oral_surgery_instance.paid + paid >= total_price:
            oral_surgery_instance.paid = total_price
        else:
            oral_surgery_instance.paid += paid  # Increment the paid amount

        oral_surgery_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(oral_surgery_instance=oral_surgery_instance, previous_date=date, paid_amount=paid,
                                         idReception1=oral_surgery_instance.idReception1, idReception=oral_surgery_instance.idReception, name=oral_surgery_instance.name,
                                         phone=oral_surgery_instance.phone, price=oral_surgery_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_oral.html', {
            'id': id,
            'oral_surgery_instance': oral_surgery_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_oral1(request, id):
    try:
        oral_surgery_instance = OralSurgery.objects.get(id=id)
    except OralSurgery.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(oral_surgery_instance=oral_surgery_instance)
    previous_date = oral_surgery_instance.date
    previous_paid = oral_surgery_instance.paid
    total_price = oral_surgery_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if oral_surgery_instance.paid + paid >= total_price:
                oral_surgery_instance.paid = total_price
            else:
                oral_surgery_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            oral_surgery_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                oral_surgery_instance=oral_surgery_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=oral_surgery_instance.idReception,
                idReception1=oral_surgery_instance.idReception1,
                name=oral_surgery_instance.name,
                phone=oral_surgery_instance.phone,
                price=oral_surgery_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_oral.html', {
        'id': id,
        'oral_surgery_instance': oral_surgery_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })


def print_oral_debt(request, id):
    try:
        oral_surgery_instance = OralSurgery.objects.get(id=id)
    except OralSurgery.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(oral_surgery_instance=oral_surgery_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = oral_surgery_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': oral_surgery_instance.name,
        'patient_phone': oral_surgery_instance.phone,
    }

    return render(request, 'debts/print_oral_debt.html', context)


@login_required
def add_endo(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)
    except Doctors.DoesNotExist:
        # Handle the case where the doctor does not exist
        return redirect('error_page')  # Redirect to an error page or handle appropriately

    if request.method == 'POST':
        form = EndoForm(request.POST, request.FILES)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception1_id = id
            price = form.cleaned_data['price']

            reception = Reception1.objects.get(id=id)
            oral_surgery.idReception_id = reception.idReception_id
            oral_surgery.name = reception.name
            oral_surgery.phone = reception.phone
            oral_surgery.gender = reception.gender
            oral_surgery.date_of_birth = reception.date_of_birth
            oral_surgery.educational_id = reception.educational_id
            oral_surgery.doctor_id = reception.doctor_id


            try:
                doctor = Doctors.objects.get(id=reception.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            # Adjust the price if price_lab is not null
            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            print(f"Original price: {price}")
            print(f"Price of lab: {price_lab}")
            print(f"Adjusted price: {adjusted_price}")

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            print(f"Doctor share: {doctor_share}")
            print(f"Center share: {center_share}")
            print(f"Total price before saving: {total_price}")

            # Assign Decimal values to model fields
            oral_surgery.doctor_share = doctor_share.quantize(Decimal('0.01'))
            oral_surgery.center_share = center_share.quantize(Decimal('0.01'))
            oral_surgery.total_price = total_price.quantize(Decimal('0.01'))
            oral_surgery.price_lab = price_lab_decimal  # Save price_lab as Decimal

            oral_surgery.save()

            photos = request.FILES.getlist('exo_images')
            endo_instance = form.save(commit=False)
            endo_instance.save()

            for photo in photos:
                Photo.objects.create(endo_instance=endo_instance, image=photo)

            return redirect('add-endo', id=id)
    else:
        reception = Reception1.objects.get(id=id)
        initial_data = {
            'idReception1_id': id,
            'idReception_id': reception.idReception_id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth,
            'educational_id': reception.educational_id,
            'doctor_id': reception.doctor_id
        }
        form = EndoForm(initial=initial_data)

    appointments = Reception1.objects.all().order_by('-id')
    oralls = Endo.objects.filter(idReception1=id)
    # Create a list to store photos for each OralSurgery instance
    photos_list = []

    try:
        orall = oralls.first()
        photos = orall.photo_set.all()
    except AttributeError:
        orall = None
        photos = None

    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None

    for orall in oralls:
        if orall.components_first:
            # Remove square brackets if they exist
            orall.components_first = orall.components_first[1:-1] if orall.components_first[0] == '[' and \
               orall.components_first[-1] == ']' else orall.components_first
        if orall.ur:
            orall.ur = orall.ur.replace("'", "")
        if orall.ul:
            orall.ul = orall.ul.replace("'", "")
        if orall.lr:
            orall.lr = orall.lr.replace("'", "")
        if orall.ll:
            orall.ll = orall.ll.replace("'", "")
        if orall.canal:
            orall.canal = orall.canal.replace("'", "")
        if orall.components_first:
            orall.components_first = orall.components_first.replace("'", "")
        if orall.components_second:
            orall.components_second = orall.components_second.replace("'", "")
        if orall.components_third:
            orall.components_third = orall.components_third.replace("'", "")
        if orall.components_fourth:
            orall.components_fourth = orall.components_fourth.replace("'", "")
        orall.price = orall.price
        orall.total_price = orall.total_price
        orall.save()
        # Retrieve photos associated with the current OralSurgery instance
        photos = orall.photo_set.all()

        # Append the photos to the photos_list
        photos_list.append(photos)

    formatted_total_prices = ["{:,.2f}".format(orall.total_price) if orall.total_price is not None else None for orall in oralls]
    formatted_prices = ["{:,.2f}".format(orall.price) if orall.price is not None else None for orall in oralls]

    return render(request, 'conservation/endo/endo.html', {
        'form': form,
        'appointments': appointments,
        'medicine': medicine,
        'oralls': oralls,
        'id': id,
        'photos': photos,
        'photos_list': photos_list,
        'formatted_total_prices': formatted_total_prices,
        'formatted_prices': formatted_prices
    })


def remove_photo_endo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    endo_instance = photo.endo_instance
    photo.delete()
    return redirect('endo-edit', id=endo_instance.id)


def delete_endo(request, id):
    # Get the drug related to the Reception
    oral = get_object_or_404(Endo, id=id)

    # Store the idReception before deleting the drug
    idReception = oral.idReception1_id

    # Delete the drug
    oral.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('add-endo', id=idReception)


def endo_reception(request):
    appointments = Reception1.objects.all().order_by('-id')
    p = Paginator(appointments,25) #Paginator
    page = request.GET.get('page') #Paginator
    appointments = p.get_page(page)#Paginator
    nums = "a" * appointments.paginator.num_pages#Paginator
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/endo/endo_reception.html', {'appointments': appointments})


def search_endo(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'conservation/endo/search_endo.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/endo/search_endo.html', {})


def endo_edit(request, id):
    orall = get_object_or_404(Endo, id=id)
    photos = Photo.objects.filter(endo_instance=orall)

    if request.method == 'POST':
        form = EndoForm(request.POST, request.FILES, instance=orall)
        if form.is_valid():
            print("Form is valid")
            price = form.cleaned_data['price']
            form_data = form.cleaned_data

            # Sanitize the fields by removing single quotes
            for field in ['ur', 'ul', 'lr', 'll']:
                form_data[field] = form_data[field].replace("'", "") if form_data[field] else None

            for field, value in form_data.items():
                setattr(orall, field, value)

            try:
                doctor = Doctors.objects.get(id=orall.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab')

            if price_lab is not None:
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price
            else:
                adjusted_price = price

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            orall.doctor_share = doctor_share.quantize(Decimal('0.01'))
            orall.center_share = center_share.quantize(Decimal('0.01'))
            orall.total_price = total_price.quantize(Decimal('0.01'))

            # Handle lab_name separately
            selected_lab = form.cleaned_data['lab_name']
            if selected_lab:
                orall.lab = selected_lab  # Set the foreign key to the selected Lab
                orall.lab_name = selected_lab.lab_name  # Save the lab_name as well
            orall.save()

            photos = request.FILES.getlist('oral_images')
            for photo in photos:
                Photo.objects.create(endo_instance=orall, image=photo)

            return redirect('add-endo', id=orall.idReception1_id)
        else:
            print("Form is not valid")
            print(form.errors)

    else:
        first_visit = orall.first_visit if orall.first_visit is not None else None
        components_first = orall.components_first if orall.components_first is not None else None
        second_visit = orall.second_visit if orall.second_visit is not None else None
        components_second = orall.components_second if orall.components_second is not None else None
        third_visit = orall.third_visit if orall.third_visit is not None else None
        components_third = orall.components_third if orall.components_third is not None else None
        fourth_visit = orall.fourth_visit if orall.fourth_visit is not None else None
        components_fourth = orall.components_fourth if orall.components_fourth is not None else None
        date = orall.date if orall.date is not None else None

        # Remove first and last characters from certain fields
        ur = orall.ur[1:-1] if orall.ur else None
        ul = orall.ul[1:-1] if orall.ul else None
        lr = orall.lr[1:-1] if orall.lr else None
        ll = orall.ll[1:-1] if orall.ll else None
        canal = orall.canal[1:-1] if orall.canal else None

        form = EndoForm(instance=orall, initial={
            'first_visit': first_visit,
            'components_first': components_first,
            'second_visit': second_visit,
            'components_second': components_second,
            'third_visit': third_visit,
            'components_third': components_third,
            'fourth_visit': fourth_visit,
            'components_fourth': components_fourth,
            'date': date,
            'ur': ur,
            'ul': ul,
            'lr': lr,
            'll': ll,
            'canal': canal,
        })
        print("Initial form data:", {
            'second_visit': form.initial.get('second_visit'),
            'third_visit': form.initial.get('third_visit'),
            'fourth_visit': form.initial.get('fourth_visit')
        })
    labs = Lab.objects.all()
    return render(request, 'conservation/endo/update_endo.html', {'form': form, 'orall': orall, 'labs': labs})


def add_debt_endo(request, id):
    try:
        endo_instance = Endo.objects.get(id=id)
    except Endo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(endo_instance=endo_instance)
    previous_date = endo_instance.date
    previous_paid = endo_instance.paid
    total_price = endo_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if endo_instance.paid + paid >= total_price:
            endo_instance.paid = total_price
        else:
            endo_instance.paid += paid  # Increment the paid amount

        endo_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(endo_instance=endo_instance, previous_date=date, paid_amount=paid,
                                         idReception1=endo_instance.idReception1, idReception=endo_instance.idReception, name=endo_instance.name,
                                         phone=endo_instance.phone, price=endo_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_endo.html', {
            'id': id,
            'endo_instance': endo_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })




def add_debt_endo1(request, id):
    try:
        endo_instance = Endo.objects.get(id=id)
    except Endo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(endo_instance=endo_instance)
    previous_date = endo_instance.date
    previous_paid = endo_instance.paid
    total_price = endo_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if endo_instance.paid + paid >= total_price:
                endo_instance.paid = total_price
            else:
                endo_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            endo_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                endo_instance=endo_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=endo_instance.idReception,
                idReception1=endo_instance.idReception1,
                name=endo_instance.name,
                phone=endo_instance.phone,
                price=endo_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_endo.html', {
        'id': id,
        'endo_instance': endo_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })


def print_endo_debt(request, id):
    try:
        endo_instance = Endo.objects.get(id=id)
    except Endo.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(endo_instance=endo_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = endo_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': endo_instance.name,
        'patient_phone': endo_instance.phone,
    }

    return render(request, 'debts/print_endo_debt.html', context)


def endo_visit(request, id):
    orall = get_object_or_404(Endo, id=id)

    if request.method == 'POST':
        form = EndoForm(request.POST, instance=orall)
        if form.is_valid():

            # Replace single quotes in certain fields
            if orall.ur:
                orall.ur = orall.ur.replace("'", "")
            if orall.ul:
                orall.ul = orall.ul.replace("'", "")
            if orall.lr:
                orall.lr = orall.lr.replace("'", "")
            if orall.ll:
                orall.ll = orall.ll.replace("'", "")

            form.save()
            return redirect('add-endo', id=orall.idReception_id)
    else:
        # Define a default value for first_visit when the request method is not POST
        first_visit = orall.first_visit if orall.first_visit else date.today()
        # Define a default value for second_visit when the request method is not POST
        components_first = orall.components_first if orall.components_first is not None else None
        second_visit = orall.second_visit if orall.second_visit is not None else None
        components_second = orall.components_second if orall.components_second is not None else None
        third_visit = orall.third_visit if orall.third_visit is not None else None
        components_third = orall.components_third if orall.components_third is not None else None
        fourth_visit = orall.fourth_visit if orall.fourth_visit is not None else None
        components_fourth = orall.components_fourth if orall.components_fourth is not None else None
        # Remove first and last characters from certain fields
        ur = orall.ur[1:-1] if orall.ur else None
        ul = orall.ul[1:-1] if orall.ul else None
        lr = orall.lr[1:-1] if orall.lr else None
        ll = orall.ll[1:-1] if orall.ll else None
        canal = orall.canal[1:-1] if orall.canal else None

        form = EndoForm(instance=orall, initial={
            'components_first': components_first,
            'second_visit': second_visit,
            'components_second': components_second,
            'third_visit': third_visit,
            'components_third': components_third,
            'fourth_visit': fourth_visit,
            'components_fourth': components_fourth,
            'ur': ur,
            'ul': ul,
            'lr': lr,
            'll': ll,
            'canal': canal,
        })

    return render(request, 'conservation/endo/endo_visit.html', {'form': form, 'orall': orall, 'first_visit': first_visit})


def edit_payment_history(request, id):
    payment_history = get_object_or_404(PaymentHistory, pk=id)
    old_paid_amount = payment_history.paid_amount  # Get the old paid amount

    if request.method == 'POST':
        form = PaymentHistoryForm(request.POST, instance=payment_history)
        if form.is_valid():
            form.save()

            # Update the paid amount in the related ortho instance
            ortho_instance = payment_history.ortho_instance
            new_paid_amount = ortho_instance.paid - (old_paid_amount - payment_history.paid_amount)
            ortho_instance.paid = new_paid_amount
            ortho_instance.save()

            ortho_instance_id = ortho_instance.id
            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            # Redirect back to the same date with start_date and end_date parameters
            return redirect(reverse('add-debt-ortho1', args=[
                ortho_instance_id]) + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

    else:
        form = PaymentHistoryForm(instance=payment_history)

    remaining_amount = payment_history.price - payment_history.paid_amount

    context = {
        'form': form,
        'idReception': payment_history.idReception_id,

        'idReception1': payment_history.idReception1_id,
        'name': payment_history.name,
        'phone': payment_history.phone,
        'price': payment_history.price,
        'paid_amount': payment_history.paid_amount,
        'crown_instance': payment_history.crown_instance_id,
        'veneer_instance': payment_history.veneer_instance_id,
        'ortho_instance': payment_history.ortho_instance_id,
        'remaining_amount': remaining_amount,
        'start_date': request.GET.get('start_date'),  # Include start_date parameter in the context
        'end_date': request.GET.get('end_date'),  # Include end_date parameter in the context
    }
    return render(request, 'debts/edit_payment_history.html', context)


def calculate_price_view(request):
    context = {}

    # Check if doctor_id is provided in the request
    doctor_id = request.GET.get('doctor_id')

    if doctor_id:
        try:
            # Fetch all Exo instances related to the doctor_id
            exo_instances = Exo.objects.filter(doctor_id=doctor_id)

            if exo_instances.exists():
                # Fetch the Doctor object associated with the doctor_id
                doctor = exo_instances.first().doctor  # Assuming each Exo has the same doctor
                # Initialize lists to store calculated values and totals
                prices = []
                total_prices = {
                    'total_total_price': Decimal('0'),
                    'total_discounted_price': Decimal('0'),
                    'total_remaining_amount': Decimal('0'),
                }

                discount_value = Decimal('0.333')  # Example discount value as Decimal (33.3%)
                remaining_value = Decimal('1') - discount_value

                # Calculate prices for each instance and accumulate totals
                for exo_instance in exo_instances:
                    total_price = exo_instance.total_price
                    discounted_price = total_price * (1 - discount_value)
                    remaining_amount = total_price * discount_value

                    # Append a dictionary with calculated values to prices list
                    prices.append({
                        'total_price': total_price,
                        'discount_value': discount_value,
                        'discounted_price': discounted_price,
                        'remaining_amount': remaining_amount,
                        'remaining_value': remaining_value,
                    })

                    # Accumulate totals
                    total_prices['total_total_price'] += total_price
                    total_prices['total_discounted_price'] += discounted_price
                    total_prices['total_remaining_amount'] += remaining_amount

                context = {
                    'prices': prices,
                    'doctor_id': doctor_id,
                    'doctor_name': doctor.doctor_name,
                    'total_prices': total_prices,  # Add total_prices to context
                }

            else:
                context['error'] = f"No Exo instances found for doctor ID '{doctor_id}'."

        except Exo.DoesNotExist:
            context['error'] = f"Doctor ID '{doctor_id}' not found."

    return render(request, 'finance/price.html', context)


def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            barcode = form.cleaned_data.get('barcode')
            new_quantity = int(form.cleaned_data.get('quantity'))  # Ensure new_quantity is an integer

            # Check if a store record with the same barcode already exists
            existing_store = Store.objects.filter(barcode=barcode).first()

            if existing_store:
                # Add the new quantity to the existing quantity
                existing_store.quantity += new_quantity  # Ensure addition of integers
                existing_store.save()
            else:
                # Create a new store record
                store = form.save(commit=False)
                store.user = request.user  # Set the logged-in user
                store.save()

            return redirect('add_store')  # Redirect to the same page after saving the form data
    else:
        form = StoreForm()

    appointments = Store.objects.all().order_by('-regdate')
    return render(request, 'store/add_store.html', {'form': form, 'appointments': appointments})


def delete_material(request,id):
    appointments = Material.objects.get(pk=id)
    appointments.delete()
    return redirect('material')

def delete_lab(request,id):
    appointments = Lab.objects.get(pk=id)
    appointments.delete()
    return redirect('lab')

def store_search(request):
    store_instance = None
    alerts = []

    if request.method == 'POST':
        barcode = request.POST.get('barcode', '')

        # Query the Store model for the given barcode
        try:
            store_instance = Store.objects.get(barcode=barcode)

            # Check expiry date condition
            current_date = datetime.now().date()
            expire_date = store_instance.expire_date

            if expire_date is not None and (expire_date - current_date) < timedelta(days=30):
                alerts.append(f'Alert: Expiry date for barcode {barcode} is less than one month.')

            # Check quantity condition
            quantity_remaining = int(store_instance.quantity)  # Convert to integer

            if quantity_remaining <= 3:
                alerts.append(f'Alert: Quantity remaining for barcode {barcode} is less than or equal to 3.')

        except Store.DoesNotExist:
            alerts.append(f'No store item found with barcode {barcode}.')
            store_instance = None

    return render(request, 'store/store_search.html', {'store_instance': store_instance, 'alerts': alerts})

@login_required
def add_material_output(request):
    total_quantity_in_store = None  # Default value if barcode is not found

    if request.method == 'POST':
        form = MaterialOutputForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            quantity = form.cleaned_data['quantity']  # Already validated and converted to integer

            try:
                store_item = Store.objects.get(barcode=barcode)
                store_item_quantity = int(store_item.quantity)  # Convert to integer
                material_name = store_item.material_name

                # Calculate total quantity already outputted for this barcode
                total_output_quantity = MaterialOutput.objects.filter(store__barcode=barcode).aggregate(Sum('quantity'))['quantity__sum']
                if total_output_quantity is None:
                    total_output_quantity = 0

                # Check if the requested quantity exceeds the available quantity in store
                if total_output_quantity + quantity > store_item_quantity:
                    messages.error(request, 'Not enough quantity in stock.')
                else:
                    material_output = form.save(commit=False)
                    material_output.store = store_item
                    material_output.user = request.user
                    material_output.material_out = material_name  # Save material name
                    material_output.quantity_in = store_item_quantity  # Save quantity in
                    material_output.save()

                    # Calculate remaining quantity in store after output
                    remaining_quantity = store_item_quantity - total_output_quantity - quantity
                    print(f"Remaining quantity: {remaining_quantity}")

                    messages.success(request, 'Material output successfully recorded.')
                    return redirect('add_material_output')  # Redirect to the same page after saving the form data

            except Store.DoesNotExist:
                messages.error(request, 'No store item found with the provided barcode.')

        else:
            messages.error(request, 'Form is not valid.')
            print(form.errors)  # Debugging

    else:
        form = MaterialOutputForm()

    # Fetch all outputs
    outputs = MaterialOutput.objects.all().order_by('-output_date')

    # Calculate remaining quantity for each output and check if less than 3
    remaining_quantities = {}
    for output in outputs:
        barcode = output.store.barcode
        if barcode not in remaining_quantities:
            remaining_quantities[barcode] = output.store.quantity
        remaining_quantities[barcode] -= output.quantity
        output.remaining_quantity = remaining_quantities[barcode]

        # Check if remaining quantity is less than 3 and set an alert
        if output.remaining_quantity < 3:
            messages.warning(request, f'Remaining quantity for barcode {barcode} is less than 3.')

    doctors = Doctors.objects.all()

    # Fetch total quantity available in store for the barcode
    if form.initial.get('barcode'):
        try:
            store_item = Store.objects.get(barcode=form.initial.get('barcode'))
            total_quantity_in_store = store_item.quantity
        except Store.DoesNotExist:
            total_quantity_in_store = None
            print(f"Total quantity in store: {total_quantity_in_store}")  # Debugging

    return render(request, 'store/add_material_output.html', {
        'form': form,
        'outputs': outputs,
        'total_quantity_in_store': total_quantity_in_store,
        'doctors': doctors,  # Pass doctors to the template
    })


def print_material_output(request, id):
    output = get_object_or_404(MaterialOutput, id=id)
    return render(request, 'store/print_material_output.html', {'output': output})


def xrays_reception(request):
    user = request.user
    try:
        if user.role == 'admin':
            appointments = Reception1.objects.all().order_by('-id')
        else:
            doctor = Doctors.objects.get(user=user)
            appointments = Reception1.objects.filter(doctor=doctor).order_by('-id')
    except Doctors.DoesNotExist:
        appointments = Reception1.objects.none()

    p = Paginator(appointments, 25)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")

    return render(request, 'xrays/xrays_reception.html', {'appointments': appointments, 'nums': nums})

def search_xrays(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'xrays/search_xrays.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'xrays/search_xrays.html', {})
@login_required
def xrays(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = XraysForm(request.POST, request.FILES)
            if form.is_valid():
                oral_surgery = form.save(commit=False)
                oral_surgery.idReception1_id = id

                price = form.cleaned_data['price']
                oral_surgery.name = reception.name
                oral_surgery.phone = reception.phone
                oral_surgery.gender = reception.gender
                oral_surgery.date_of_birth = reception.date_of_birth
                oral_surgery.educational_id = reception.educational_id
                oral_surgery.idReception_id = reception.idReception_id
                oral_surgery.doctor_id = reception.doctor_id

                oral_surgery.total_price = price
                oral_surgery.save()

                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(xrays_instance=oral_surgery, image=photo)

                return redirect('xrays', id=id)
            else:
                form = XraysForm(initial={
                    'idReception1_id': id,
                    'name': reception.name,
                    'phone': reception.phone,
                    'gender': reception.gender,
                    'date_of_birth': reception.date_of_birth,
                    'educational_id': reception.educational_id,
                    'idReception_id': reception.idReception_id,
                    'doctor_id': reception.doctor_id
                })
        else:
            form = XraysForm(initial={
                'idReception1_id': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'idReception_id': reception.idReception_id,
                'doctor_id': reception.doctor_id
            })

        appointments = Reception1.objects.all().order_by('-id')
        exooes = Xrays.objects.filter(idReception1=id)
        photos_list = []

        exoo = exooes.first()
        photos = exoo.photo_set.all() if exoo else None

        medicine = Medicin.objects.filter(idReception=id).first()

        for exoo in exooes:
            if exoo.ur:
                exoo.ur = exoo.ur.replace("'", "")
            if exoo.ul:
                exoo.ul = exoo.ul.replace("'", "")
            if exoo.lr:
                exoo.lr = exoo.lr.replace("'", "")
            if exoo.ll:
                exoo.ll = exoo.ll.replace("'", "")
            exoo.total_price = exoo.price
            exoo.save()
            photos = exoo.photo_set.all()
            photos_list.append(photos)

        formatted_total_prices = ["{:,}".format(exoo.total_price) if exoo.total_price is not None else None for exoo in exooes]
        formatted_prices = ["{:,}".format(exoo.price) if exoo.price is not None else None for exoo in exooes]

        return render(request, 'xrays/xrays.html', {
            'form': form,
            'appointments': appointments,
            'medicine': medicine,
            'exooes': exooes,
            'id': id,
            'photos': photos,
            'photos_list': photos_list,
            'formatted_total_prices': formatted_total_prices,
            'reception': reception,
            'formatted_prices': formatted_prices
        })
    except Doctors.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    except Reception1.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'Reception does not exist or you do not have permission to access it.')
        return redirect('home')

def delete_xrays(request, id):
    # Get the drug related to the Reception
    exo = get_object_or_404(Xrays, id=id)

    # Store the idReception before deleting the drug
    idReception = exo.idReception1_id

    # Delete the drug
    exo.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('xrays', id=idReception)

def xrays_edit(request, id):
    exoo = get_object_or_404(Xrays, id=id)
    photos = Photo.objects.filter(xrays_instance=exoo)

    if request.method == 'POST':
        form = XraysForm(request.POST, request.FILES, instance=exoo)
        if form.is_valid():
            exoo = form.save(commit=False)
            price = form.cleaned_data['price']

            exoo.save()

            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(xrays_instance=exoo, image=photo)

            return redirect('xrays', id=exoo.idReception1_id)
    else:
        form = XraysForm(instance=exoo)

    return render(request, 'xrays/xrays_edit.html', {'form': form, 'id': id, 'exoo': exoo, 'photos': photos})


def print_xrays_debt1(request, id):
    try:
        xrays_instance = Xrays.objects.get(id=id)
    except Xrays.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(xrays_instance=xrays_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = xrays_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': xrays_instance.name,
        'patient_phone': xrays_instance.phone,
    }

    return render(request, 'debts/print_xrays_debt1.html', context)


def all_debts_xrays(request):
    form = SearchForm(request.GET or None)  # Instantiate the form

    # Initialize selected_doctor with None
    selected_doctor = None

    if request.method == 'GET':
        if form.is_valid():
            # Use the correct parameter name based on your URL
            selected_doctor = form.cleaned_data['doctor']

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_datetime = None  # Initialize start_datetime variable
    end_datetime = None  # Initialize end_datetime variable

    exos = Xrays.objects.none()  # Initialize as an empty queryset

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_datetime = end_datetime + timedelta(days=1)

        date_range_filter = Q(regdate__range=(start_datetime, end_datetime))
        doctor_filter = Q(doctor=selected_doctor) if selected_doctor else Q()

        exos = Xrays.objects.filter(date_range_filter & doctor_filter)

    search_results = []

    if exos.exists():
        search_results.append(('Xrays', exos))
    total_exo2 = exos.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    # Calculate total paid for each type
    paid_exo = exos.aggregate(paid=Sum('paid'))['paid'] or 0
    total_price_t2 = total_exo2
    total_paid_t = paid_exo
    remaining = total_price_t2 - total_paid_t

    context = {
        'form': form,
        'search_results': search_results,
        'total_exo2': total_exo2,
        'paid_exo': paid_exo,
        'total_price_t2': total_price_t2,
        'total_paid_t': total_paid_t,
        'remaining': remaining,
        'start_date': start_date,  # Add this line
        'end_date': end_date  # Add this line
    }

    return render(request, 'debts/all_debts_xrays.html', context)


def add_debt_xrays1(request, id):
    try:
        xrays_instance = Xrays.objects.get(id=id)
    except Xrays.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(xrays_instance=xrays_instance)
    previous_date = xrays_instance.date
    previous_paid = xrays_instance.paid
    total_price = xrays_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if xrays_instance.paid + paid >= total_price:
                xrays_instance.paid = total_price
            else:
                xrays_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            xrays_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                xrays_instance=xrays_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=xrays_instance.idReception,
                name=xrays_instance.name,
                phone=xrays_instance.phone,
                price=xrays_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts_xrays') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_xrays.html', {
        'id': id,
        'xrays_instance': xrays_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })

@login_required
def surgery_reception(request):
    user = request.user
    try:
        if user.role == 'admin':
            appointments = Reception1.objects.all().order_by('-id')
        else:
            doctor = Doctors.objects.get(user=user)
            appointments = Reception1.objects.filter(doctor=doctor).order_by('-id')
    except Doctors.DoesNotExist:
        appointments = Reception1.objects.none()

    p = Paginator(appointments, 25)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")

    return render(request, 'surgery/surgery_reception.html', {'appointments': appointments, 'nums': nums})
def search_surgery(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'surgery/search_surgery.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'surgery/search_surgery.html', {})

@login_required
def surgery(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = SurgeryForm(request.POST, request.FILES)
            if form.is_valid():
                oral_surgery = form.save(commit=False)
                oral_surgery.idReception1_id = id

                price = form.cleaned_data['price']
                oral_surgery.name = reception.name
                oral_surgery.phone = reception.phone
                oral_surgery.gender = reception.gender
                oral_surgery.date_of_birth = reception.date_of_birth
                oral_surgery.educational_id = reception.educational_id
                oral_surgery.idReception_id = reception.idReception_id
                oral_surgery.doctor_id = reception.doctor_id

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                oral_surgery.doctor_share = doctor_share.quantize(Decimal('0.01'))
                oral_surgery.center_share = center_share.quantize(Decimal('0.01'))
                oral_surgery.price_lab = price_lab_decimal.quantize(Decimal('0.01'))
                oral_surgery.total_price = total_price.quantize(Decimal('0.01'))  # Save total_price as Decimal

                # Debugging statement to confirm the assignment
                print(f"Total price after quantize: {oral_surgery.total_price}")

                oral_surgery.save()

                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(surgery_instance=oral_surgery, image=photo)

                return redirect('surgery', id=id)
            else:
                form = SurgeryForm(initial={
                    'idReception1_id': id,
                    'name': reception.name,
                    'phone': reception.phone,
                    'gender': reception.gender,
                    'date_of_birth': reception.date_of_birth,
                    'educational_id': reception.educational_id,
                    'idReception_id': reception.idReception_id,
                    'doctor_id': reception.doctor_id
                })
        else:
            form = SurgeryForm(initial={
                'idReception1_id': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'idReception_id': reception.idReception_id,
                'doctor_id': reception.doctor_id
            })

        appointments = Reception1.objects.all().order_by('-id')
        exooes = Surgery.objects.filter(idReception1=id)
        photos_list = []

        exoo = exooes.first()
        photos = exoo.photo_set.all() if exoo else None

        medicine = Medicin.objects.filter(idReception=id).first()

        for exoo in exooes:
            if exoo.ur:
                exoo.ur = exoo.ur.replace("'", "")
            if exoo.ul:
                exoo.ul = exoo.ul.replace("'", "")
            if exoo.lr:
                exoo.lr = exoo.lr.replace("'", "")
            if exoo.ll:
                exoo.ll = exoo.ll.replace("'", "")
            exoo.total_price = exoo.total_price
            exoo.save()
            photos = exoo.photo_set.all()
            photos_list.append(photos)

        formatted_total_prices = ["{:,}".format(exoo.total_price) if exoo.total_price is not None else None for exoo in exooes]
        formatted_prices = ["{:,}".format(exoo.price) if exoo.price is not None else None for exoo in exooes]

        return render(request, 'surgery/surgery.html', {
            'form': form,
            'appointments': appointments,
            'medicine': medicine,
            'exooes': exooes,
            'id': id,
            'photos': photos,
            'photos_list': photos_list,
            'formatted_total_prices': formatted_total_prices,
            'reception': reception,
            'formatted_prices': formatted_prices
        })
    except Doctors.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    except Reception1.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'Reception does not exist or you do not have permission to access it.')
        return redirect('home')


def surgery_edit(request, id):
    exoo = get_object_or_404(Surgery, id=id)
    photos = Photo.objects.filter(surgery_instance=exoo)

    if request.method == 'POST':
        form = SurgeryForm(request.POST, request.FILES, instance=exoo)
        if form.is_valid():
            exoo = form.save(commit=False)
            price = form.cleaned_data['price']

            try:
                doctor = Doctors.objects.get(id=exoo.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            exoo.doctor_share = doctor_share.quantize(Decimal('0.01'))
            exoo.center_share = center_share.quantize(Decimal('0.01'))
            exoo.total_price = total_price.quantize(Decimal('0.01'))
            exoo.save()

            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(surgery_instance=exoo, image=photo)

            return redirect('surgery', id=exoo.idReception1_id)
    else:
        form = SurgeryForm(instance=exoo)

    labs = Lab.objects.all()
    return render(request, 'surgery/surgery_edit.html', {'form': form, 'id': id, 'exoo': exoo, 'photos': photos, 'labs': labs})


def remove_photo_surgery(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    surgery_instance = photo.surgery_instance
    photo.delete()
    return redirect('surgery_edit', id=surgery_instance.id)

def delete_surgery(request, id):
    # Get the drug related to the Reception
    exo = get_object_or_404(Surgery, id=id)

    # Store the idReception before deleting the drug
    idReception = exo.idReception1_id

    # Delete the drug
    exo.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('surgery', id=idReception)


def print_surgery_debt1(request, id):
    try:
        surgery_instance = Surgery.objects.get(id=id)
    except Surgery.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(surgery_instance=surgery_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = surgery_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': surgery_instance.name,
        'patient_phone': surgery_instance.phone,
    }

    return render(request, 'debts/print_surgery_debt1.html', context)


def add_debt_surgery(request, id):
    try:
        surgery_instance = Surgery.objects.get(id=id)
    except Surgery.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(surgery_instance=surgery_instance)
    previous_date = surgery_instance.date
    previous_paid = surgery_instance.paid
    total_price = surgery_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if surgery_instance.paid + paid >= total_price:
            surgery_instance.paid = total_price
        else:
            surgery_instance.paid += paid  # Increment the paid amount

        surgery_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(surgery_instance=surgery_instance, previous_date=date, paid_amount=paid,
                                         idReception1=surgery_instance.idReception1, idReception=surgery_instance.idReception, name=surgery_instance.name,
                                         phone=surgery_instance.phone, price=surgery_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_surgery.html', {
            'id': id,
            'surgery_instance': surgery_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_surgery1(request, id):
    try:
        surgery_instance = Surgery.objects.get(id=id)
    except Surgery.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(surgery_instance=surgery_instance)
    previous_date = surgery_instance.date
    previous_paid = surgery_instance.paid
    total_price = surgery_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if surgery_instance.paid + paid >= total_price:
                surgery_instance.paid = total_price
            else:
                surgery_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            surgery_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                surgery_instance=surgery_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=surgery_instance.idReception,
                idReception1=surgery_instance.idReception1,
                name=surgery_instance.name,
                phone=surgery_instance.phone,
                price=surgery_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_surgery.html', {
        'id': id,
        'surgery_instance': surgery_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })

def print_surgery_debt(request, id):
    debts = PaymentHistory.objects.filter(idReception1=id)

    # Calculate the total remaining amount for idReception
    total_exo = Exo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_filling = Filling.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_crown = Crown.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_endo = Endo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_ortho = Ortho.objects.filter(idReception1=id).aggregate(total_price=Sum('price'))['total_price'] or 0

    total_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_surgery = Surgery.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))[
                               'total_price'] or 0

    paid_exo = Exo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_filling = Filling.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_crown = Crown.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_endo = Endo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_ortho = Ortho.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_surgery = Surgery.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))[
                              'total_paid'] or 0

    total_price = (total_exo + total_filling + total_crown + total_veneer + total_oralSurgery + total_endo + total_ortho + total_periodontology + total_prosthodontics+ total_surgery)
    total_paid = (paid_exo + paid_filling + paid_crown + paid_veneer + paid_oralSurgery + paid_endo + paid_ortho + paid_periodontology + paid_prosthodontics+ paid_surgery)
    total_remaining = total_price - total_paid



    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_exo': total_exo,  # Add total_salary to the context
        'total_filling': total_filling,  # Add total_salary to the context
        'total_crown': total_crown,  # Add total_salary to the context
        'total_veneer': total_veneer,  # Add total_salary to the context
        'total_oralSurgery': total_oralSurgery,  # Add total_salary to the context
        'total_endo': total_endo,  # Add total_salary to the context
        'total_ortho': total_ortho,  # Add total_salary to the context
        'total_periodontology': total_periodontology,  # Add total_salary to the context
        'total_prosthodontics': total_prosthodontics,  # Add total_salary to the context
        'total_surgery': total_surgery,  # Add total_salary to the context
        'paid_exo': paid_exo,  # Add total_salary to the context
        'paid_filling': paid_filling,  # Add total_salary to the context
        'paid_crown': paid_crown,  # Add paid_salary to the context
        'paid_veneer': paid_veneer,  # Add paid_salary to the context
        'paid_oralSurgery': paid_oralSurgery,  # Add paid_salary to the context
        'paid_endo': paid_endo,  # Add paid_salary to the context
        'paid_ortho': paid_ortho,  # Add paid_salary to the context
        'paid_periodontology': paid_periodontology,  # Add paid_salary to the context
        'paid_prosthodontics': paid_prosthodontics,  # Add paid_salary to the context
        'paid_surgery': paid_surgery,  # Add paid_salary to the context

    }

    return render(request, 'debts/print_surgery_debt.html', context)

@login_required
def preventive_reception(request):
    user = request.user
    try:
        if user.role == 'admin':
            appointments = Reception1.objects.all().order_by('-id')
        else:
            doctor = Doctors.objects.get(user=user)
            appointments = Reception1.objects.filter(doctor=doctor).order_by('-id')
    except Doctors.DoesNotExist:
        appointments = Reception1.objects.none()

    p = Paginator(appointments, 25)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")

    return render(request, 'preventive/preventive_reception.html', {'appointments': appointments, 'nums': nums})


def search_preventive(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception1.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception1.objects.all()
        return render(request, 'preventive/search_preventive.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'preventive/search_preventive.html', {})

@login_required
def preventive(request, id):
    user = request.user

    try:
        # Check if the user is an admin
        if user.role == 'admin':
            reception = get_object_or_404(Reception1, id=id)
        else:
            # Get the doctor instance associated with the logged-in user
            doctor = Doctors.objects.get(user=user)
            # Get the reception instance and ensure it belongs to the logged-in doctor
            reception = get_object_or_404(Reception1, id=id, doctor=doctor)

        if request.method == 'POST':
            form = PreventiveForm(request.POST, request.FILES)
            if form.is_valid():
                oral_surgery = form.save(commit=False)
                oral_surgery.idReception1_id = id

                price = form.cleaned_data['price']
                oral_surgery.name = reception.name
                oral_surgery.phone = reception.phone
                oral_surgery.gender = reception.gender
                oral_surgery.date_of_birth = reception.date_of_birth
                oral_surgery.educational_id = reception.educational_id
                oral_surgery.idReception_id = reception.idReception_id
                oral_surgery.doctor_id = reception.doctor_id

                try:
                    doctor = Doctors.objects.get(id=reception.doctor_id)
                    proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                    proportion_center = Decimal(doctor.proportion_center) / 100
                except (ObjectDoesNotExist, InvalidOperation):
                    proportion_doctor = Decimal('0')
                    proportion_center = Decimal('0')

                discount_option = form.cleaned_data['discount_option']
                price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

                # Adjust the price if price_lab is not null
                try:
                    price_lab_decimal = Decimal(price_lab)
                    adjusted_price = price - price_lab_decimal
                except InvalidOperation:
                    adjusted_price = price

                print(f"Original price: {price}")
                print(f"Price of lab: {price_lab}")
                print(f"Adjusted price: {adjusted_price}")

                if discount_option == 'Without Discount':
                    doctor_share = adjusted_price * proportion_doctor
                    center_share = adjusted_price * proportion_center
                    total_price = price
                elif discount_option == 'None':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price
                    total_price = center_share
                elif discount_option == 'With Discount':
                    doctor_share = Decimal('0')
                    center_share = adjusted_price * proportion_center
                    total_price = center_share + price_lab
                elif discount_option == 'Full Discount':
                    doctor_share = -1 * (adjusted_price * proportion_doctor)
                    center_share = Decimal('0')
                    total_price = price_lab
                elif discount_option == 'No Pay':
                    doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                    center_share = Decimal('0')
                    total_price = center_share
                else:
                    doctor_share = Decimal('0')
                    center_share = Decimal('0')
                    total_price = Decimal('0')

                print(f"Doctor share: {doctor_share}")
                print(f"Center share: {center_share}")
                print(f"Total price before saving: {total_price}")

                # Assign Decimal values to model fields
                oral_surgery.doctor_share = doctor_share.quantize(Decimal('0.01'))
                oral_surgery.center_share = center_share.quantize(Decimal('0.01'))
                oral_surgery.price_lab = price_lab_decimal.quantize(Decimal('0.01'))
                oral_surgery.total_price = total_price.quantize(Decimal('0.01'))  # Save total_price as Decimal

                # Debugging statement to confirm the assignment
                print(f"Total price after quantize: {oral_surgery.total_price}")

                oral_surgery.save()

                photos = request.FILES.getlist('exo_images')
                for photo in photos:
                    Photo.objects.create(preventive_instance=oral_surgery, image=photo)

                return redirect('preventive', id=id)
            else:
                form = PreventiveForm(initial={
                    'idReception1_id': id,
                    'name': reception.name,
                    'phone': reception.phone,
                    'gender': reception.gender,
                    'date_of_birth': reception.date_of_birth,
                    'educational_id': reception.educational_id,
                    'idReception_id': reception.idReception_id,
                    'doctor_id': reception.doctor_id
                })
        else:
            form = PreventiveForm(initial={
                'idReception1_id': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth,
                'educational_id': reception.educational_id,
                'idReception_id': reception.idReception_id,
                'doctor_id': reception.doctor_id
            })

        appointments = Reception1.objects.all().order_by('-id')
        exooes = Preventive.objects.filter(idReception1=id)
        photos_list = []

        exoo = exooes.first()
        photos = exoo.photo_set.all() if exoo else None

        medicine = Medicin.objects.filter(idReception=id).first()

        for exoo in exooes:
            if exoo.ur:
                exoo.ur = exoo.ur.replace("'", "")
            if exoo.ul:
                exoo.ul = exoo.ul.replace("'", "")
            if exoo.lr:
                exoo.lr = exoo.lr.replace("'", "")
            if exoo.ll:
                exoo.ll = exoo.ll.replace("'", "")
            exoo.total_price = exoo.total_price
            exoo.save()
            photos = exoo.photo_set.all()
            photos_list.append(photos)

        formatted_total_prices = ["{:,}".format(exoo.total_price) if exoo.total_price is not None else None for exoo in exooes]
        formatted_prices = ["{:,}".format(exoo.price) if exoo.price is not None else None for exoo in exooes]

        return render(request, 'preventive/preventive.html', {
            'form': form,
            'appointments': appointments,
            'medicine': medicine,
            'exooes': exooes,
            'id': id,
            'photos': photos,
            'photos_list': photos_list,
            'formatted_total_prices': formatted_total_prices,
            'reception': reception,
            'formatted_prices': formatted_prices
        })
    except Doctors.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    except Reception1.DoesNotExist:
        # Redirect to an error page or show a message
        messages.error(request, 'Reception does not exist or you do not have permission to access it.')
        return redirect('home')


def preventive_edit(request, id):
    exoo = get_object_or_404(Preventive, id=id)
    photos = Photo.objects.filter(preventive_instance=exoo)

    if request.method == 'POST':
        form = PreventiveForm(request.POST, request.FILES, instance=exoo)
        if form.is_valid():
            exoo = form.save(commit=False)
            price = form.cleaned_data['price']

            try:
                doctor = Doctors.objects.get(id=exoo.doctor_id)
                proportion_doctor = Decimal(doctor.proportion_doctor) / 100
                proportion_center = Decimal(doctor.proportion_center) / 100
            except (ObjectDoesNotExist, InvalidOperation):
                proportion_doctor = Decimal('0')
                proportion_center = Decimal('0')

            discount_option = form.cleaned_data['discount_option']
            price_lab = form.cleaned_data.get('price_lab') or Decimal('0')

            try:
                price_lab_decimal = Decimal(price_lab)
                adjusted_price = price - price_lab_decimal
            except InvalidOperation:
                adjusted_price = price

            if discount_option == 'Without Discount':
                doctor_share = adjusted_price * proportion_doctor
                center_share = adjusted_price * proportion_center
                total_price = price
            elif discount_option == 'None':
                doctor_share = Decimal('0')
                center_share = adjusted_price
                total_price = center_share
            elif discount_option == 'With Discount':
                doctor_share = Decimal('0')
                center_share = adjusted_price * proportion_center
                total_price = center_share + price_lab
            elif discount_option == 'Full Discount':
                doctor_share = -1 * (adjusted_price * proportion_doctor)
                center_share = Decimal('0')
                total_price = price_lab
            elif discount_option == 'No Pay':
                doctor_share = -1 * (adjusted_price * proportion_doctor) - price_lab
                center_share = Decimal('0')
                total_price = center_share
            else:
                doctor_share = Decimal('0')
                center_share = Decimal('0')
                total_price = Decimal('0')

            exoo.doctor_share = doctor_share.quantize(Decimal('0.01'))
            exoo.center_share = center_share.quantize(Decimal('0.01'))
            exoo.total_price = total_price.quantize(Decimal('0.01'))
            exoo.save()

            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(preventive_instance=exoo, image=photo)

            return redirect('preventive', id=exoo.idReception1_id)
    else:
        form = PreventiveForm(instance=exoo)

    labs = Lab.objects.all()
    return render(request, 'preventive/preventive_edit.html', {'form': form, 'id': id, 'exoo': exoo, 'photos': photos, 'labs': labs})


def remove_photo_preventive(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    preventive_instance = photo.preventive_instance
    photo.delete()
    return redirect('preventive_edit', id=preventive_instance.id)


def delete_preventive(request, id):
    # Get the drug related to the Reception
    exo = get_object_or_404(Preventive, id=id)

    # Store the idReception before deleting the drug
    idReception = exo.idReception1_id

    # Delete the drug
    exo.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('preventive', id=idReception)


def print_preventive_debt1(request, id):
    try:
        preventive_instance = Preventive.objects.get(id=id)
    except Preventive.DoesNotExist:
        return HttpResponse("Crown instance not found")

    debts = PaymentHistory.objects.filter(preventive_instance=preventive_instance)

    # Calculate the total remaining amount for the crown
    total_paid = debts.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_price = preventive_instance.total_price
    total_remaining = total_price - total_paid

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_paid': total_paid,
        'patient_name': preventive_instance.name,
        'patient_phone': preventive_instance.phone,
    }

    return render(request, 'debts/print_preventive_debt1.html', context)


def add_debt_preventive(request, id):
    try:
        preventive_instance = Preventive.objects.get(id=id)
    except Preventive.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(preventive_instance=preventive_instance)
    previous_date = preventive_instance.date
    previous_paid = preventive_instance.paid
    total_price = preventive_instance.total_price

    if request.method == 'POST':
        paid = Decimal(request.POST.get('paid', '0'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        if preventive_instance.paid + paid >= total_price:
            preventive_instance.paid = total_price
        else:
            preventive_instance.paid += paid  # Increment the paid amount

        preventive_instance.save()

        # Store the previous date from the form in PaymentHistory
        payment_history = PaymentHistory(preventive_instance=preventive_instance, previous_date=date, paid_amount=paid,
                                         idReception1=preventive_instance.idReception1, idReception=preventive_instance.idReception, name=preventive_instance.name,
                                         phone=preventive_instance.phone, price=preventive_instance.total_price)
        payment_history.save()

        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        remaining_amount = total_price - previous_paid

        return render(request, 'debts/add_debt_preventive.html', {
            'id': id,
            'preventive_instance': preventive_instance,
            'previous_dates': previous_dates,
            'previous_paid': previous_paid,
            'remaining_amount': remaining_amount
        })


def add_debt_preventive1(request, id):
    try:
        preventive_instance = Preventive.objects.get(id=id)
    except Preventive.DoesNotExist:
        return HttpResponse("Crown instance not found")

    previous_dates = PaymentHistory.objects.filter(preventive_instance=preventive_instance)
    previous_date = preventive_instance.date
    previous_paid = preventive_instance.paid
    total_price = preventive_instance.total_price

    if request.method == 'POST':
        paid = request.POST.get('paid', '0')
        print("Received Paid Value:", paid)  # Debug line: print received value

        try:
            paid = Decimal(paid)  # Convert to Decimal

            if preventive_instance.paid + paid >= total_price:
                preventive_instance.paid = total_price
            else:
                preventive_instance.paid += paid  # Increment the paid amount (both are Decimal now)

            preventive_instance.save()

            # Store the previous date from the form in PaymentHistory
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            payment_history = PaymentHistory(
                preventive_instance=preventive_instance,
                previous_date=date,
                paid_amount=paid,
                idReception=preventive_instance.idReception,
                idReception1=preventive_instance.idReception1,
                name=preventive_instance.name,
                phone=preventive_instance.phone,
                price=preventive_instance.total_price
            )
            payment_history.save()

            return redirect(reverse(
                'all_debts') + f'?start_date={request.GET.get("start_date")}&end_date={request.GET.get("end_date")}')

        except Exception as e:
            print("Conversion Error:", e)  # Debug line: print any conversion errors
            # Handle the error appropriately or log it for further investigation

    # If it's not a POST request or if an error occurred, render the form
    remaining_amount = total_price - previous_paid
    return render(request, 'debts/add_debt_preventive.html', {
        'id': id,
        'preventive_instance': preventive_instance,
        'previous_dates': previous_dates,
        'previous_paid': previous_paid,
        'remaining_amount': remaining_amount
    })

def print_preventive_debt(request, id):
    debts = PaymentHistory.objects.filter(idReception1=id)

    # Calculate the total remaining amount for idReception
    total_exo = Exo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_filling = Filling.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_crown = Crown.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_endo = Endo.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_ortho = Ortho.objects.filter(idReception1=id).aggregate(total_price=Sum('price'))['total_price'] or 0

    total_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    total_surgery = Surgery.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))[
                               'total_price'] or 0
    total_preventive = Preventive.objects.filter(idReception1=id).aggregate(total_price=Sum('total_price'))[
                        'total_price'] or 0

    paid_exo = Exo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_filling = Filling.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_crown = Crown.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_veneer = Veneer.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_oralSurgery = OralSurgery.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_endo = Endo.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_ortho = Ortho.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_periodontology = Periodontology.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_prosthodontics = Prosthodontics.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0

    paid_surgery = Surgery.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))[
                              'total_paid'] or 0
    paid_preventive = Preventive.objects.filter(idReception1=id).aggregate(total_paid=Sum('paid'))[
                       'total_paid'] or 0

    total_price = (total_exo + total_filling + total_crown + total_veneer + total_oralSurgery + total_endo + total_ortho + total_periodontology + total_prosthodontics+ total_surgery+ total_preventive)
    total_paid = (paid_exo + paid_filling + paid_crown + paid_veneer + paid_oralSurgery + paid_endo + paid_ortho + paid_periodontology + paid_prosthodontics+ paid_surgery+ paid_preventive)
    total_remaining = total_price - total_paid



    context = {
        'debts': debts,
        'total_remaining': total_remaining,
        'total_price': total_price,
        'total_exo': total_exo,  # Add total_salary to the context
        'total_filling': total_filling,  # Add total_salary to the context
        'total_crown': total_crown,  # Add total_salary to the context
        'total_veneer': total_veneer,  # Add total_salary to the context
        'total_oralSurgery': total_oralSurgery,  # Add total_salary to the context
        'total_endo': total_endo,  # Add total_salary to the context
        'total_ortho': total_ortho,  # Add total_salary to the context
        'total_periodontology': total_periodontology,  # Add total_salary to the context
        'total_prosthodontics': total_prosthodontics,  # Add total_salary to the context
        'total_surgery': total_surgery,  # Add total_salary to the context
        'total_preventive': total_preventive,  # Add total_salary to the context
        'paid_exo': paid_exo,  # Add total_salary to the context
        'paid_filling': paid_filling,  # Add total_salary to the context
        'paid_crown': paid_crown,  # Add paid_salary to the context
        'paid_veneer': paid_veneer,  # Add paid_salary to the context
        'paid_oralSurgery': paid_oralSurgery,  # Add paid_salary to the context
        'paid_endo': paid_endo,  # Add paid_salary to the context
        'paid_ortho': paid_ortho,  # Add paid_salary to the context
        'paid_periodontology': paid_periodontology,  # Add paid_salary to the context
        'paid_prosthodontics': paid_prosthodontics,  # Add paid_salary to the context
        'paid_surgery': paid_surgery,  # Add paid_salary to the context
        'paid_preventive': paid_preventive,  # Add paid_salary to the context

    }

    return render(request, 'debts/print_preventive_debt.html', context)
