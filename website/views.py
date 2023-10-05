
from django.shortcuts import render,redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, AppointmentForm,DentistDetailsForm,ReceptionForm,OralSurgeryForm,OrthodonticsForm,ExoForm,\
    MedicinForm,PhotoForm,DrugForm,CrownForm,Medicine1Form,VeneerForm,FillingForm,DrugFormSet,DoctorsForm,SearchForm,\
    ImplantForm,GaveAppointmentForm,DebtsForm,BasicInfoForm,SalaryForm,OutcomeForm
from .models import Appointment1,DentistDetails,Reception,OralSurgery,Orthodontics,Exo,Medicin,\
    Photo,Drug,Medicine1,Crown,Veneer,Filling,Doctors,Implant,GaveAppointment,Debts,BasicInfo,Salary,Outcome
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date
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

    if query:
        exos = Exo.objects.filter(name=query)
        fillings = Filling.objects.filter(name=query)
        crowns = Crown.objects.filter(name=query)
        veneers = Veneer.objects.filter(name=query)
        oralSurgery = OralSurgery.objects.filter(name=query)

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

    context = {
        'query': query,
        'search_results': search_results,
    }

    return render(request, 'search.html', context)


def search_debts(request):
    query = request.GET.get('query')  # Get the search query

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()

    if query:
        exos = Exo.objects.filter(Q(name=query) | Q(phone=query))
        fillings = Filling.objects.filter(Q(name=query) | Q(phone=query))
        crowns = Crown.objects.filter(Q(name=query) | Q(phone=query))
        veneers = Veneer.objects.filter(Q(name=query) | Q(phone=query))
        oralSurgery = OralSurgery.objects.filter(Q(name=query) | Q(phone=query))

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

    context = {
        'query': query,
        'search_results': search_results,
    }

    return render(request, 'finance/search_debts.html', context)


def all_debts(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        exos = Exo.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        fillings = Filling.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        crowns = Crown.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        veneers = Veneer.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        oralSurgery = OralSurgery.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))

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

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'search_results': search_results,
    }

    return render(request, 'debts/all_debts.html', context)


def all_total(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()
    outcomes = Outcome.objects.none()
    salaries = Salary.objects.none()

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        exos = Exo.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        fillings = Filling.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        crowns = Crown.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        veneers = Veneer.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        oralSurgery = OralSurgery.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        outcomes = Outcome.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))
        salaries = Salary.objects.filter(Q(regdate__gte=start_datetime, regdate__lte=end_datetime))

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
    if outcomes.exists():
        search_results.append(('Outcome', outcomes))
    if salaries.exists():
        search_results.append(('Salary', salaries))
    total_exo = Exo.objects.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_filling = Filling.objects.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_crown = Crown.objects.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_veneer = Veneer.objects.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_oralSurgery = OralSurgery.objects.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    total_salary = salaries.aggregate(total_final_salary=Sum('finalSalary'))['total_final_salary'] or 0
    total_outcome = Outcome.objects.aggregate(total_price=Sum('price'))['total_price'] or 0
    remaining = ((total_exo+total_filling+total_crown+total_veneer+total_oralSurgery)-(total_salary+total_outcome))

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'search_results': search_results,
        'total_exo': total_exo,  # Add total_salary to the context
        'total_filling': total_filling,  # Add total_salary to the context
        'total_crown': total_crown,  # Add total_salary to the context
        'total_veneer': total_veneer,  # Add total_salary to the context
        'total_oralSurgery': total_oralSurgery,  # Add total_salary to the context
        'total_salary': total_salary,  # Add total_salary to the context
        'total_outcome': total_outcome,  # Add total_salary to the context
        'remaining': remaining,  # Add total_salary to the context
    }

    return render(request, 'all_total.html', context)


def doctor(request):
    if request.method == 'POST':
        form = DoctorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor')  # Redirect to the same page after saving the form data
    else:
        form = DoctorsForm()
    # Retrieve all Medicine1 objects (appointments) from the database and order them by their IDs in descending order.
    appointments = Doctors.objects.all().order_by('-id')
    return render(request, 'doctors/doctor.html', {'form': form, 'appointments': appointments})


def delete_doctor(request,id):
    appointments = Doctors.objects.get(pk=id)
    appointments.delete()
    return redirect('doctor')


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
            instance = form.save(commit=False)
            doctor_name = form.cleaned_data['doctor']
            instance.doctor = Doctors.objects.get(doctor_name=doctor_name)

            app_data = request.POST.get('app_data')
            days = request.POST.get('days')
            selected_times = request.POST.getlist('time')

            # Check if the same combination of app_data, days, and time exists for the selected doctor
            if Reception.objects.filter(doctor=instance.doctor, app_data=app_data, days=days,
                                        time=selected_times).exists():
                messages.error(request,
                               f'This date, days, and time are already booked for {doctor_name}.<br/> You Can Choose another Time')
                return redirect('home')

            instance.app_data = app_data
            instance.days = days
            instance.time = selected_times  # Set the time value
            instance.save()
            # Redirect to 'home' after successful form submission
            # Assuming selected_times is a list of times, for example:
            selected_times = request.POST.getlist('time')

            # Join the list elements into a string with a comma separator
            times_str = ', '.join(selected_times)
            messages.success(request, f'Appointment successfully booked for {app_data}, {days},  at {times_str}.')
            return redirect('home')  # Redirect after successful form submissionat {times_str}

    else:
        form = ReceptionForm()

    appointments = Reception.objects.all().order_by('-id')
    # Clean appointments data before rendering
    cleaned_appointments = []
    for appointment in appointments:
        if appointment.days:
            appointment.days = appointment.days.replace("'", "")
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
        cleaned_appointments.append(appointment)

    return render(request, 'home.html', {'form': form, 'appointments': appointments})


def search_doctor(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            selected_doctor = form.cleaned_data['doctor']
            receptions = Reception.objects.filter(doctor=selected_doctor).order_by('-app_data')
            # Clean appointments data before rendering
            cleaned_receptions = []
            for reception in receptions:
                if reception.days:
                    reception.days = reception.days.replace("'", "")
                if reception.time:
                    reception.time = reception.time.replace("'", "")
                cleaned_receptions.append(reception)

            return render(request, 'doctors/search_doctor.html', {'receptions': receptions, 'form': form})
    else:
        form = SearchForm()
        receptions = Reception.objects.all().order_by('-app_data')
        cleaned_receptions = []
        for reception in receptions:
            if reception.days:
                reception.days = reception.days.replace("'", "")
            if reception.time:
                reception.time = reception.time.replace("'", "")
            cleaned_receptions.append(reception)

    return render(request, 'doctors/search_doctor.html', {'form': form,'receptions': receptions})


def all_reception(request):
    appointments = Reception.objects.all().order_by('-id')
    for appointment in appointments:
        if appointment.days:
            appointment.days = appointment.days.replace("'", "")
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")

    return render(request, 'all_reception.html', {'appointments': appointments})


def delete_reception(request, id):
    appointments = Reception.objects.get(pk=id)
    appointments.delete()
    return redirect('all-reception')


def update_reception(request, id):
    pi = Reception.objects.get(pk=id)
    form = ReceptionForm(request.POST or None, instance=pi)
    if form.is_valid():
        form.save()
        return redirect('all-reception')
    return render(request, 'update_reception.html', {'form': form, 'pi': pi})


def gave_appointment(request, id):
    # Check if the request method is POST
    if request.method == 'POST':
        # Initialize the form with the submitted POST data
        form = ReceptionForm(request.POST)
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
            # Check if the same combination of app_data, days, and time exists in the database
            if Reception.objects.filter(app_data=app_data, days=days, time=selected_times).exists():
                messages.error(request, 'This date, days, and time are already booked. You can choose another Time.')
                return redirect('gave-appointment', id=id)

            # Retrieve the existing Reception instance with the provided ID
            existing_reception = Reception.objects.get(id=id)

            # Set the instance fields using existing data and new values
            instance.idReception_id = id
            instance.name = existing_reception.name
            instance.phone = existing_reception.phone
            instance.gender = existing_reception.gender
            instance.date_of_birth = existing_reception.date_of_birth
            instance.app_data = app_data
            instance.days = days
            instance.time = selected_times

            # Save the new instance to the database
            instance.save()
            # Redirect to 'home' after successful form submission
            messages.success(request, f'Appointment successfully booked for {app_data}, {days}, {selected_times}.')
            # Redirect to 'home' after successful form submission
            return redirect('gave-appointment', id=id)
    else:
        # Retrieve the existing Reception instance with the provided ID
        existing_reception = Reception.objects.get(id=id)

        # Populate the form with initial data from the existing instance
        initial_data = {
            'idReception': id,
            'name': existing_reception.name,
            'phone': existing_reception.phone,
            'gender': existing_reception.gender,
            'date_of_birth': existing_reception.date_of_birth
        }
        form = ReceptionForm(initial=initial_data)

    # Retrieve all Reception instances from the database
    appointments = Reception.objects.all().order_by('-id')

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


def all_gave(request):
    gaves = Reception.objects.all().order_by('-id')
    # Clean appointments data before rendering
    cleaned_gaves = []
    for gave in gaves:
        if gave.days:
            gave.days = gave.days.replace("'", "")
        if gave.time:
            gave.time = gave.time.replace("'", "")
        cleaned_gaves.append(gave)
    return render(request, 'all_gave.html', {'gaves': gaves})


def add_oral_surgery(request, id):
    if request.method == 'POST':
        form = OralSurgeryForm(request.POST, request.FILES)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            implant_name = form.cleaned_data['implant']
            oral_surgery.implant = Implant.objects.get(implant_name=implant_name)
            oral_surgery.idReception_id = id
            no_unite = form.cleaned_data['no_unite']
            price = form.cleaned_data['price']
            total_price = no_unite * price
            oral_surgery.total_price = total_price
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name
            oral_surgery.phone = reception.phone
            oral_surgery.gender = reception.gender
            oral_surgery.date_of_birth = reception.date_of_birth
            oral_surgery.save()

            photos = request.FILES.getlist('exo_images')
            oral_surgery_instance = form.save(commit=False)
            oral_surgery_instance.save()

            for photo in photos:
                Photo.objects.create(oral_surgery_instance=oral_surgery_instance, image=photo)

            return redirect('add-oral-surgery', id=id)
        else:
            reception = Reception.objects.get(id=id)
            initial_data = {
                'idReception': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth
            }
            form = OralSurgeryForm(initial=initial_data)
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = OralSurgeryForm(initial=initial_data)

    appointments = Reception.objects.all().order_by('-id')
    oralls = OralSurgery.objects.filter(idReception=id)
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
        if orall.ur:
            orall.ur = orall.ur.replace("'", "")
        if orall.ul:
            orall.ul = orall.ul.replace("'", "")
        if orall.lr:
            orall.lr = orall.lr.replace("'", "")
        if orall.ll:
            orall.ll = orall.ll.replace("'", "")
        orall.total_price = orall.no_unite * orall.price
        orall.save()
        # Retrieve photos associated with the current OralSurgery instance
        photos = orall.photo_set.all()

        # Append the photos to the photos_list
        photos_list.append(photos)

    formatted_total_prices = ["{:,.2f}".format(orall.total_price) if orall.total_price is not None else None for orall in oralls]
    formatted_prices = ["{:,.2f}".format(orall.price) if orall.price is not None else None for orall in oralls]

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
    idReception = oral.idReception_id

    # Delete the drug
    oral.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('add-oral-surgery', id=idReception)


def oral_reception(request):
    appointments = Reception.objects.all().order_by('-id')
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'oral_reception.html', {'appointments': appointments})


def search_oral(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception.objects.all()
        return render(request, 'search_oral_surgery.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'search_oral_surgery.html', {})


def oral_edit(request, id):
    orall = get_object_or_404(OralSurgery, id=id)

    if request.method == 'POST':
        form = OralSurgeryForm(request.POST, instance=orall)
        if form.is_valid():
            form.save()
            return redirect('add-oral-surgery', id=orall.idReception_id)  # Redirect to a success view after saving
    else:
        initial_data = {
            'first_visit': orall.first_visit,
            'second_visit': orall.second_visit,
            'third_visit': orall.third_visit,
            'fourth_visit': orall.fourth_visit,
            'fifth_visit': orall.fifth_visit,
            'ur': orall.ur[1:-1] if orall.ur else None,
            'ul': orall.ul[1:-1] if orall.ul else None,
            'lr': orall.lr[1:-1] if orall.lr else None,
            'll': orall.ll[1:-1] if orall.ll else None,
        }

    form = OralSurgeryForm(instance=orall, initial=initial_data)

    return render(request, 'update_oral_surgery.html', {'form': form, 'orall': orall})



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


def orthodontics(request):
    if request.method == 'POST':
        form = OrthodonticsForm(request.POST)
        if form.is_valid():
            orthodontics = form.save(commit=False)
            orthodontics.material_field = form.cleaned_data['material_field']
            orthodontics.width_field = form.cleaned_data['width_field']
            orthodontics.save()
            return redirect('reception')  # Redirect to a success page after form submission
    else:
        form = OrthodonticsForm()
    return render(request, 'orthodontic.html', {'form': form})


def exo_reception(request):
    appointments =Reception.objects.all().order_by('-id')
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'exo/exo_reception.html', {'appointments': appointments})


def exo_reception1(request):
    appointments =Reception.objects.all().order_by('-id')
    return render(request, 'exo/exo_reception1.html', {'appointments': appointments})


def exo(request, id):
    if request.method == 'POST':
        form = ExoForm(request.POST, request.FILES)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id

            price = form.cleaned_data['price']
            total_price = price
            oral_surgery.total_price = total_price
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name
            oral_surgery.phone = reception.phone
            oral_surgery.gender = reception.gender
            oral_surgery.date_of_birth = reception.date_of_birth
            oral_surgery.save()

            photos = request.FILES.getlist('exo_images')
            exo_instance = form.save(commit=False)
            exo_instance.save()

            for photo in photos:
                Photo.objects.create(exo_instance=exo_instance, image=photo)

            return redirect('exo', id=id)
        else:
            reception = Reception.objects.get(id=id)
            initial_data = {
                'idReception': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth

            }
            form = ExoForm(initial=initial_data)
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = ExoForm(initial=initial_data)

    appointments = Reception.objects.all().order_by('-id')
    exooes = Exo.objects.filter(idReception=id)
    # Create a list to store photos for each OralSurgery instance
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
        if exoo.exoby:
            exoo.exoby = exoo.exoby.replace("'", "")
        if exoo.simpleexo:
            exoo.simpleexo = exoo.simpleexo.replace("'", "")
        if exoo.complcated:
            exoo.complcated = exoo.complcated.replace("'", "")
        exoo.total_price = exoo.price
        exoo.save()
        # Retrieve photos associated with the current OralSurgery instance
        photos = exoo.photo_set.all()

        # Append the photos to the photos_list
        photos_list.append(photos)

    formatted_total_prices = ["{:,.2f}".format(exoo.total_price) if exoo.total_price is not None else None for exoo in exooes]
    formatted_prices = ["{:,.2f}".format(exoo.price) if exoo.price is not None else None for exoo in exooes]

    return render(request, 'exo/exo.html', {
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


def exo_edit(request, id):
    pi = Exo.objects.get(id=id)
    photos = Photo.objects.filter(exo_instance=pi)  # Fetch photos associated with the oral surgery instance
    exoo = None  # Initialize orall to None
    if request.method == 'POST':
        form = ExoForm(request.POST, instance=pi)
        if form.is_valid():
            # Calculate total_price
            price = form.cleaned_data['price']
            total_price = price

            form.instance.total_price = total_price  # Set the 'total_price' field of the form instance
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(exo_instance=pi, image=photo)

            return redirect('exo', id=pi.idReception_id)
    else:
        form = ExoForm(instance=pi)
        try:
            exoo = Exo.objects.get(idReception=id)
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
            if exoo.exoby:
                exoo.exoby = exoo.exoby.replace("'", "")
            if exoo.simpleexo:
                exoo.simpleexo = exoo.simpleexo.replace("'", "")
            if exoo.complcated:
                exoo.complcated = exoo.complcated.replace("'", "")
        except Exo.DoesNotExist:
            exoo = None
            photos = None

    return render(request, 'exo/exo_edit.html', {'form': form, 'id': id, 'exoo': exoo, 'photos': photos})


def remove_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    exo_instance = photo.exo_instance
    photo.delete()
    return redirect('exo_edit', id=exo_instance.id)


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
        appointment.simpleexo = appointment.simpleexo.replace("'", "")
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
        orals = Reception.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception.objects.all()
        return render(request, 'exo/search_exo.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'exo/search_exo.html', {})


def search_exo1(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception.objects.all()
        return render(request, 'exo/search_exo1.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'exo/search_exo1.html', {})


def delete_exo(request, id):
    # Get the drug related to the Reception
    exo = get_object_or_404(Exo, id=id)

    # Store the idReception before deleting the drug
    idReception = exo.idReception_id

    # Delete the drug
    exo.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('exo', id=idReception)


def drugs(request, id):
    reception = get_object_or_404(Reception, id=id)

    if request.method == 'POST':
        form = DrugForm(request.POST)
        formset = DrugFormSet(request.POST, prefix='drugs')

        if form.is_valid() and formset.is_valid():
            drugs = form.save(commit=False)
            drugs.idReception_id = id
            drugs.name = reception.name
            drugs.phone = reception.phone
            drugs.gender = reception.gender
            drugs.date_of_birth = reception.date_of_birth
            drugs.save()

            for drug_form in formset:
                if drug_form.cleaned_data.get('name_medicine'):
                    drug = drug_form.save(commit=False)
                    drug.idReception_id = id
                    drug.name = reception.name
                    drug.phone = reception.phone
                    drug.gender = reception.gender
                    drug.date_of_birth = reception.date_of_birth
                    drug.name_medicine = drug_form.cleaned_data['name_medicine'].name_medicine
                    drug.save()

            return redirect('drugs', id=id)
    else:
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = DrugForm(initial=initial_data)
        formset = DrugFormSet(prefix='drugs')

    appointments = Reception.objects.all().order_by('-id')
    try:
        medicines = Drug.objects.filter(idReception=id)
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
    idReception = drug.idReception_id

    # Delete the drug
    drug.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('drugs', id=idReception)


def print_drugs(request, id):
    drugs = Drug.objects.filter(idReception=id)
    context = {
        'drugs': drugs,
    }
    return render(request, 'drugs/print_drugs.html', context)


def crown_reception(request):
    appointments =Reception.objects.all().order_by('-id')
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/crown/crown_reception.html', {'appointments': appointments})


def search_crown(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception.objects.all()
        return render(request, 'conservation/crown/search_crown.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/crown/search_crown.html', {})


def crown(request, id):
    if request.method == 'POST':
        form = CrownForm(request.POST, request.FILES)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']
            total_price = no_prepare * price
            oral_surgery.total_price = total_price
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name
            oral_surgery.phone = reception.phone
            oral_surgery.gender = reception.gender
            oral_surgery.date_of_birth = reception.date_of_birth
            oral_surgery.save()

            photos = request.FILES.getlist('exo_images')
            crown_instance = form.save(commit=False)
            crown_instance.save()

            for photo in photos:
                Photo.objects.create(crown_instance=crown_instance, image=photo)

            return redirect('crown', id=id)
        else:
            reception = Reception.objects.get(id=id)
            initial_data = {
                'idReception': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth
            }
            form = CrownForm(initial=initial_data)
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = CrownForm(initial=initial_data)

    appointments = Reception.objects.all().order_by('-id')
    crownn = Crown.objects.filter(idReception=id)
    photos_list = []

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

    for crown in crownn:
        photos = crown.photo_set.all()
        photos_list.append(photos)

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
            total_price = no_prepare * price

            form.instance.total_price = total_price  # Set the 'total_price' field of the form instance
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(crown_instance=pi, image=photo)

            return redirect('crown', id=pi.idReception_id)
    else:
        form = CrownForm(instance=pi)

    return render(request, 'conservation/crown/crown_edit.html', {'form': form, 'pi': pi, 'photos': photos})


def remove_photo_crown(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    crown_instance = photo.crown_instance
    photo.delete()
    return redirect('crown_edit', id=crown_instance.id)


def delete_crown(request, id):
    # Get the drug related to the Reception
    crown = get_object_or_404(Crown, id=id)

    # Store the idReception before deleting the drug
    idReception = crown.idReception_id

    # Delete the drug
    crown.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('crown', id=idReception)


def veneer_reception(request):
    appointments =Reception.objects.all().order_by('-id')
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/veneer/veneer_reception.html', {'appointments': appointments})


def search_veneer(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception.objects.all()
        return render(request, 'conservation/veneer/search_veneer.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/veneer/search_veneer.html', {})


def veneer(request, id):
    if request.method == 'POST':
        form = VeneerForm(request.POST, request.FILES)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']
            total_price = no_prepare * price
            oral_surgery.total_price = total_price
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name
            oral_surgery.phone = reception.phone
            oral_surgery.gender = reception.gender
            oral_surgery.date_of_birth = reception.date_of_birth
            oral_surgery.save()

            photos = request.FILES.getlist('exo_images')
            veneer_instance = form.save(commit=False)
            veneer_instance.save()

            for photo in photos:
                Photo.objects.create(veneer_instance=veneer_instance, image=photo)

            return redirect('veneer', id=id)
        else:
            reception = Reception.objects.get(id=id)
            initial_data = {
                'idReception': id,
                'name': reception.name,
                'phone': reception.phone,
                'gender': reception.gender,
                'date_of_birth': reception.date_of_birth
            }
            form = VeneerForm(initial=initial_data)
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = VeneerForm(initial=initial_data)

    appointments = Reception.objects.all().order_by('-id')
    veneerr = Veneer.objects.filter(idReception=id)
    photos_list = []

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

    for veneer in veneerr:
        photos = veneer.photo_set.all()
        photos_list.append(photos)

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
            total_price = no_prepare * price

            form.instance.total_price = total_price  # Set the 'total_price' field of the form instance
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(veneer_instance=pi, image=photo)

            return redirect('veneer', id=pi.idReception_id)
    else:
        form = VeneerForm(instance=pi)

    return render(request, 'conservation/veneer/veneer_edit.html', {'form': form, 'pi': pi, 'photos': photos})


def delete_veneer(request, id):
    # Get the drug related to the Reception
    veneer = get_object_or_404(Veneer, id=id)

    # Store the idReception before deleting the drug
    idReception = veneer.idReception_id

    # Delete the drug
    veneer.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('veneer', id=idReception)


def remove_photo_veneer(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    veneer_instance = photo.veneer_instance
    photo.delete()
    return redirect('veneer_edit', id=veneer_instance.id)


def filling(request, id):
    if request.method == 'POST':
        form = FillingForm(request.POST, request.FILES)
        if form.is_valid():
            filling_instance = form.save(commit=False)
            filling_instance.idReception_id = id
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']
            total_price = no_prepare * price
            filling_instance.total_price = total_price

            reception = Reception.objects.get(id=id)
            filling_instance.name = reception.name
            filling_instance.phone = reception.phone
            filling_instance.gender = reception.gender
            filling_instance.date_of_birth = reception.date_of_birth
            filling_instance.save()

            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(filling_instance=filling_instance, image=photo)

            return redirect('filling', id=id)
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = FillingForm(initial=initial_data)

    appointments = Reception.objects.all().order_by('-id')
    fillingg = Filling.objects.filter(idReception=id)
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
        if fill.filling_place:
            fill.filling_place = fill.filling_place.replace("'", "")
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

    formatted_total_prices = ["{:,.2f}".format(fill.total_price) if fill.total_price is not None else None for fill in
                              fillingg]
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


def filling_reception(request):
    appointments =Reception.objects.all().order_by('-id')
    for appointment in appointments:
        if appointment.time:
            appointment.time = appointment.time.replace("'", "")
    return render(request, 'conservation/filling/filling_reception.html', {'appointments': appointments})


def search_filling(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = Reception.objects.filter(Q(name__icontains=searched) | Q(phone__icontains=searched))
        receptions = Reception.objects.all()
        return render(request, 'conservation/filling/search_filling.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'conservation/filling/search_filling.html', {})


def filling_edit(request, id):
    pi = Filling.objects.get(id=id)
    photos = Photo.objects.filter(filling_instance=pi)  # Fetch photos associated with the exo instance

    if request.method == 'POST':
        form = FillingForm(request.POST, instance=pi)
        if form.is_valid():
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']
            total_price = no_prepare * price

            form.instance.total_price = total_price  # Set the 'total_price' field of the form instance
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(filling_instance=pi, image=photo)

            return redirect('filling', id=pi.idReception_id)
    else:
        form = FillingForm(instance=pi)

    return render(request, 'conservation/filling/filling_edit.html', {'form': form, 'pi': pi, 'photos': photos})


def delete_filling(request, id):
    # Get the drug related to the Reception
    filling = get_object_or_404(Filling, id=id)

    # Store the idReception before deleting the drug
    idReception = filling.idReception_id

    # Delete the drug
    filling.delete()

    # Redirect to the 'drugs' view with the same idReception
    return redirect('filling', id=idReception)


def remove_photo_filling(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    filling_instance = photo.filling_instance
    photo.delete()
    return redirect('filling_edit', id=filling_instance.id)


def add_debt(request, id):
    try:
        exo_instance = Exo.objects.get(id=id)
    except Exo.DoesNotExist:
        return HttpResponse("Exo instance not found")

    if request.method == 'POST':
        paid = request.POST.get('paid')
        exo_instance.paid = paid
        exo_instance.save()

        # Redirect back to the 'search-debts' page with the same query parameter
        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        return render(request, 'debts/add_debt.html', {'id': id, 'exo_instance': exo_instance})


def print_exo_debt(request, id):
    debts = Exo.objects.filter(idReception=id)

    # Calculate the total remaining amount for idReception
    total_remaining = sum(debt.total_price - debt.paid for debt in debts)

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
    }

    template_name = 'debts/print_exo_debt.html'  # Replace with your template name

    # Redirect to the PDF generation view
    return crown_pdf(request, template_name, context)


def add_debt_crown(request, id):
    try:
        crown_instance = Crown.objects.get(id=id)
    except Crown.DoesNotExist:
        return HttpResponse("Crown instance not found")

    if request.method == 'POST':
        paid = request.POST.get('paid')
        crown_instance.paid = paid
        crown_instance.save()

        # Redirect back to the 'search-debts' page with the same query parameter
        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        return render(request, 'debts/add_debt_crown.html', {'id': id, 'crown_instance': crown_instance})


def print_crown_debt(request, id):
    debts = Crown.objects.filter(idReception=id)

    # Calculate the total remaining amount for idReception
    total_remaining = sum(debt.total_price - debt.paid for debt in debts)

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
    }
    template_name = 'debts/print_crown_debt.html'  # Replace with your template name

    # Redirect to the PDF generation view
    return crown_pdf(request, template_name, context)


def add_debt_filling(request, id):
    try:
        filling_instance = Filling.objects.get(id=id)
    except Filling.DoesNotExist:
        return HttpResponse("Filling instance not found")

    if request.method == 'POST':
        paid = request.POST.get('paid')
        filling_instance.paid = paid
        filling_instance.save()

        # Redirect back to the 'search-debts' page with the same query parameter
        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        return render(request, 'debts/add_debt_filling.html', {'id': id, 'filling_instance': filling_instance})


def print_filling_debt(request, id):
    debts = Filling.objects.filter(idReception=id)

    # Calculate the total remaining amount for idReception
    total_remaining = sum(debt.total_price - debt.paid for debt in debts)

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
    }

    return render(request, 'debts/print_filling_debt.html', context)


def add_debt_veneer(request, id):
    try:
        veneer_instance = Veneer.objects.get(id=id)
    except Veneer.DoesNotExist:
        return HttpResponse("Veneer instance not found")

    if request.method == 'POST':
        paid = request.POST.get('paid')
        veneer_instance.paid = paid
        veneer_instance.save()

        # Redirect back to the 'search-debts' page with the same query parameter
        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        return render(request, 'debts/add_debt_veneer.html', {'id': id, 'veneer_instance': veneer_instance})


def print_veneer_debt(request, id):
    debts = Veneer.objects.filter(idReception=id)

    # Calculate the total remaining amount for idReception
    total_remaining = sum(debt.total_price - debt.paid for debt in debts)

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
    }
    template_name = 'debts/print_veneer_debt.html'  # Replace with your template name

    # Redirect to the PDF generation view
    return generate_pdf_view(request, template_name, context)


def add_debt_oral(request, id):
    try:
        oral_surgery_instance = OralSurgery.objects.get(id=id)
    except OralSurgery.DoesNotExist:
        return HttpResponse("OralSurgery instance not found")

    if request.method == 'POST':
        paid = request.POST.get('paid')
        oral_surgery_instance.paid = paid
        oral_surgery_instance.save()

        # Redirect back to the 'search-debts' page with the same query parameter
        return redirect(reverse('search-debts') + f'?query={request.GET.get("query")}')
    else:
        return render(request, 'debts/add_debt_oral.html', {'id': id, 'oral_surgery_instance': oral_surgery_instance})


def print_oral_debt(request, id):
    debts = OralSurgery.objects.filter(idReception=id)

    # Calculate the total remaining amount for idReception
    total_remaining = sum(debt.total_price - debt.paid for debt in debts)

    context = {
        'debts': debts,
        'total_remaining': total_remaining,
    }
    template_name = 'debts/print_oral_debt.html'  # Replace with your template name

    # Redirect to the PDF generation view
    return generate_pdf_view(request, template_name, context)
