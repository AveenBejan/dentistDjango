from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, AppointmentForm,DentistDetailsForm,ReceptionForm,OralSurgeryForm,OrthodonticsForm,ExoForm,\
    MedicinForm,PhotoForm,DrugForm,CrownForm,Medicine1Form,VeneerForm,FillingForm,DrugFormSet,DoctorsForm,SearchForm,ImplantForm,GaveAppointmentForm
from .models import Appointment1,DentistDetails,Reception,OralSurgery,Orthodontics,Exo,Medicin,\
    Photo,Drug,Medicine1,Crown,Veneer,Filling,Doctors,Implant,GaveAppointment
from django.db.models import Q
from django.shortcuts import redirect
from django.forms import formset_factory
from django.db import transaction
from django.urls import reverse
from datetime import date
from django.contrib import messages


def search_view(request):
    query = request.GET.get('query')  # Get the search query

    exos = Exo.objects.none()  # Initialize as an empty queryset
    fillings = Filling.objects.none()
    crowns = Crown.objects.none()
    veneers = Veneer.objects.none()
    oralSurgery = OralSurgery.objects.none()

    if query:
        exos = Exo.objects.filter(name__icontains=query)
        fillings = Filling.objects.filter(name__icontains=query)
        crowns = Crown.objects.filter(name__icontains=query)
        veneers = Veneer.objects.filter(name__icontains=query)
        oralSurgery = OralSurgery.objects.filter(name__icontains=query)

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


def report_view(request):
    exos = Exo.objects.all()
    crowns = Crown.objects.all()
    fillings = Filling.objects.all()
    veneers = Veneer.objects.all()

    combined_data = zip(exos, crowns, fillings, veneers)

    context = {
        'combined_data': combined_data,
    }

    return render(request, 'report.html', context)


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

            # Check if the same combination of app_data, days, and time exists in the database
            if Reception.objects.filter(app_data=app_data, days=days, time=selected_times).exists():
                messages.error(request, 'This date, days, and time are already booked.<br/> You Can Choose another Date')
                return redirect('home')

            instance.app_data = app_data
            instance.days = days
            instance.time = selected_times  # Set the time value
            instance.save()

            return redirect('home')  # Redirect after successful form submission
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
            receptions = Reception.objects.filter(doctor=selected_doctor, app_data=date.today())
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
        receptions = Reception.objects.all().order_by('-id')

    return render(request, 'doctors/search_doctor.html', {'form': form,'receptions': receptions})


def all_reception(request):
    appointments = Reception.objects.all().order_by('-id')
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
                messages.error(request,
                               'This date, days, and time are already booked.<br/> You Can Choose another Date')
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
            return redirect('home')
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
    pi = OralSurgery.objects.get(id=id)
    photos = Photo.objects.filter(oral_surgery_instance=pi)  # Fetch photos associated with the oral surgery instance
    orall = None  # Initialize orall to None
    if request.method == 'POST':
        form = OralSurgeryForm(request.POST, instance=pi)
        if form.is_valid():
            # Calculate total_price
            no_unite = form.cleaned_data['no_unite']
            price = form.cleaned_data['price']
            total_price = no_unite * price

            form.instance.total_price = total_price  # Set the 'total_price' field of the form instance
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(oral_surgery_instance=pi, image=photo)

            return redirect('add-oral-surgery', id=pi.idReception_id)
    else:
        form = OralSurgeryForm(instance=pi)
        try:
            orall = OralSurgery.objects.get(idReception=id)
            photos = orall.photo_set.all()
            # Sanitize field values in the instance
            if orall.ur:
                orall.ur = orall.ur.replace("'", "")
            if orall.ul:
                orall.ul = orall.ul.replace("'", "")
            if orall.lr:
                orall.lr = orall.lr.replace("'", "")
            if orall.ll:
                orall.ll = orall.ll.replace("'", "")
        except OralSurgery.DoesNotExist:
            orall = None
            photos = None

    return render(request, 'update_oral_surgery.html', {'form': form, 'pi': pi, 'orall': orall, 'photos': photos})


def oral_visit(request, id):
    pi = OralSurgery.objects.get(id=id)
    photos = Photo.objects.filter(oral_surgery_instance=pi)  # Fetch photos associated with the oral surgery instance
    orall = None  # Initialize orall to None
    if request.method == 'POST':
        form = OralSurgeryForm(request.POST, instance=pi)
        if form.is_valid():
            # Calculate total_price
            no_unite = form.cleaned_data['no_unite']
            price = form.cleaned_data['price']
            total_price = no_unite * price

            form.instance.total_price = total_price  # Set the 'total_price' field of the form instance
            form.save()

            # Update the associated photos
            photos = request.FILES.getlist('exo_images')
            for photo in photos:
                Photo.objects.create(oral_surgery_instance=pi, image=photo)

            return redirect('add-oral-surgery', id=pi.idReception_id)
    else:
        form = OralSurgeryForm(instance=pi)
        try:
            orall = OralSurgery.objects.get(idReception=id)
            photos = orall.photo_set.all()
            # Sanitize field values in the instance
            if orall.ur:
                orall.ur = orall.ur.replace("'", "")
            if orall.ul:
                orall.ul = orall.ul.replace("'", "")
            if orall.lr:
                orall.lr = orall.lr.replace("'", "")
            if orall.ll:
                orall.ll = orall.ll.replace("'", "")
        except OralSurgery.DoesNotExist:
            orall = None
            photos = None

    return render(request, 'oral_visit.html', {'form': form, 'pi': pi, 'orall': orall,'photos': photos})


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
            no_prepare = form.cleaned_data['no_prepare']
            price = form.cleaned_data['price']
            total_price = no_prepare * price

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
            oral_surgery.idReception_id = id  # Set the foreign key to the specified 'id'
            no_prepare = form.cleaned_data['no_prepare']

            # Assuming 'price' is also coming from the form, get its value as well
            price = form.cleaned_data['price']

            # Calculate the total price
            total_price = no_prepare * price

            # Set the 'total_price' field of the model instance
            oral_surgery.total_price = total_price

            total_price = no_prepare * price
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name  # Set the name from Reception model
            oral_surgery.phone = reception.phone  # Set the name from Reception model
            oral_surgery.gender = reception.gender  # Set the gender from Reception model
            oral_surgery.date_of_birth = reception.date_of_birth  # Set the gender from Reception model
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
        form = CrownForm(initial=initial_data)  # Prepopulate the form with initial data
    appointments = Reception.objects.all().order_by('-id')

    try:
        crownn = Crown.objects.get(idReception=id)
        photos = crownn.photo_set.all()
    except Crown.DoesNotExist:
        crownn = None
        photos = None
    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None
    # Calculate the formatted total_price with commas as thousands separators
    formatted_total_price = "{:,.2f}".format(crownn.total_price) if crownn else None
    formatted_price = "{:,.2f}".format(crownn.price) if crownn else None
    return render(request, 'conservation/crown/crown.html', {'form': form, 'appointments': appointments, 'medicine': medicine,
                'crownn': crownn, 'id': id,'photos': photos, 'formatted_total_price': formatted_total_price,'formatted_price': formatted_price})


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
            oral_surgery.idReception_id = id  # Set the foreign key to the specified 'id'
            no_prepare = form.cleaned_data['no_prepare']

            # Assuming 'price' is also coming from the form, get its value as well
            price = form.cleaned_data['price']

            # Calculate the total price
            total_price = no_prepare * price

            # Set the 'total_price' field of the model instance
            oral_surgery.total_price = total_price

            total_price = no_prepare * price
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name  # Set the name from Reception model
            oral_surgery.phone = reception.phone  # Set the name from Reception model
            oral_surgery.gender = reception.gender  # Set the gender from Reception model
            oral_surgery.date_of_birth = reception.date_of_birth  # Set the gender from Reception model
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
        form = VeneerForm(initial=initial_data)  # Prepopulate the form with initial data
    appointments = Reception.objects.all().order_by('-id')

    try:
        veneerr = Veneer.objects.get(idReception=id)
        photos = veneerr.photo_set.all()
    except Veneer.DoesNotExist:
        veneerr = None
        photos = None
    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None
        # Calculate the formatted total_price with commas as thousands separators
    formatted_total_price = "{:,.2f}".format(veneerr.total_price) if veneerr else None
    formatted_price = "{:,.2f}".format(veneerr.price) if veneerr else None

    return render(request, 'conservation/veneer/veneer.html',
                  {'form': form, 'appointments': appointments, 'medicine': medicine, 'veneerr': veneerr, 'id': id,
                   'photos': photos, 'formatted_total_price': formatted_total_price,'formatted_price':formatted_price})


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
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id  # Set the foreign key to the specified 'id'
            no_prepare = form.cleaned_data['no_prepare']

            # Assuming 'price' is also coming from the form, get its value as well
            price = form.cleaned_data['price']

            # Calculate the total price
            total_price = no_prepare * price

            # Set the 'total_price' field of the model instance
            oral_surgery.total_price = total_price

            total_price = no_prepare * price
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name  # Set the name from Reception model
            oral_surgery.phone = reception.phone  # Set the name from Reception model
            oral_surgery.gender = reception.gender  # Set the gender from Reception model
            oral_surgery.date_of_birth = reception.date_of_birth  # Set the gender from Reception model
            oral_surgery.save()
            photos = request.FILES.getlist('exo_images')

            filling_instance = form.save(commit=False)
            filling_instance.save()

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
        form = FillingForm(initial=initial_data)  # Prepopulate the form with initial data

    appointments = Reception.objects.all().order_by('-id')

    try:
        fillingg = Filling.objects.get(idReception=id)
        photos = fillingg.photo_set.all()
    except Filling.DoesNotExist:
        fillingg = None
        photos = None
    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None
        # Replace commas in Exo model fields
    if fillingg:
        if fillingg.ur:
            fillingg.ur = fillingg.ur.replace("'", "")
        if fillingg.ul:
            fillingg.ul = fillingg.ul.replace("'", "")
        if fillingg.lr:
            fillingg.lr = fillingg.lr.replace("'", "")
        if fillingg.ll:
            fillingg.ll = fillingg.ll.replace("'", "")
    # Calculate the formatted total_price with commas as thousands separators
    formatted_total_price = "{:,.2f}".format(fillingg.total_price) if fillingg else None
    formatted_price = "{:,.2f}".format(fillingg.price) if fillingg else None
    return render(request, 'conservation/filling/filling.html', {'form': form, 'appointments': appointments, 'medicine': medicine,
                                            'fillingg': fillingg, 'id': id,'photos': photos,
                                                                 'formatted_total_price':formatted_total_price,'formatted_price':formatted_price})


def filling_reception(request):
    appointments =Reception.objects.all().order_by('-id')
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