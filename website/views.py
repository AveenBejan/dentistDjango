from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, AppointmentForm,DentistDetailsForm,ReceptionForm,OralSurgeryForm,OrthodonticsForm,ExoForm,MedicinForm
from .models import Appointment1,DentistDetails,Reception,OralSurgery,Orthodontics,Exo,Medicin
import pdfkit
from django.template.loader import render_to_string
from wkhtmltopdf.views import PDFTemplateView


def home(request):
    return render(request, 'home.html')


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
            form.save()
            appointments = Reception.objects.all().order_by('-id')
            return render(request, 'exo/exo_reception.html', {'form': form, 'appointments': appointments})
    else:
        form = ReceptionForm()
        return render(request, 'home.html')


def all_reception(request):
    appointments = Reception.objects.all().order_by('-id')
    return render(request, 'all_reception.html', {'appointments': appointments})


def delete_reception(request, id):
    appointments = Reception.objects.get(pk=id)
    appointments.delete()
    return redirect('all-reception')


def update_reception(request, id):
    pi = Reception.objects.get(pk=id)
    form = ReceptionForm(request.POST or None,  instance=pi)
    if form.is_valid():
        form.save()
        return redirect('all-reception')
    return render(request,'update_reception.html',{'form':form,'pi':pi})


def add_oral_surgery(request, id):
    if request.method == 'POST':
        form = OralSurgeryForm(request.POST)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id  # Set the foreign key to the specified 'id'
            oral_surgery.save()
            return redirect('all-oral-surgery')
    else:
        form = OralSurgeryForm(initial={'idReception': id})  # Prepopulate the form with 'id' value
    receptions = Reception.objects.all().order_by('-id')
    return render(request, 'index.html', {'form': form, 'receptions': receptions, 'id': id})


def oral_reception(request):
    receptions = Reception.objects.all().order_by('-id')
    return render(request, 'oral_reception.html', {'receptions': receptions})


def search_oral_surgery(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        orals = OralSurgery.objects.filter(idReception__name__icontains=searched)
        receptions = Reception.objects.all()
        return render(request, 'search_oral_surgery.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'search_oral_surgery.html', {})


def updateee_oral_surgery(request, id):
    pi = OralSurgery.objects.get(pk=id)
    form = OralSurgeryForm(request.POST, instance=pi)
    if form.is_valid():
            form.save()
            return redirect('all-oral-surgery')
    else:
        pi = OralSurgery.objects.get(pk=id)
        form = OralSurgeryForm(instance=pi)
    return render(request, 'update_oral_surgery.html', {'form': form, 'pi': pi})


def all_oral_surgery(request):
    orals = OralSurgery.objects.all().order_by('-id')
    return render(request, 'all_oral_surgery.html', {'orals': orals})


def delete_orla_surgery(request, id):
    orals = OralSurgery.objects.get(pk=id)
    orals.delete()
    return redirect('all-oral-surgery')


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


def exo(request, id):
    if request.method == 'POST':
        form = ExoForm(request.POST)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id  # Set the foreign key to the specified 'id'
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name  # Set the name from Reception model
            oral_surgery.phone = reception.phone  # Set the name from Reception model
            oral_surgery.gender = reception.gender  # Set the gender from Reception model
            oral_surgery.date_of_birth = reception.date_of_birth  # Set the gender from Reception model
            oral_surgery.save()
            return redirect('all-exo')
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = ExoForm(initial=initial_data)  # Prepopulate the form with initial data

    appointments = Reception.objects.all().order_by('-id')
    try:
        exoo = Exo.objects.get(idReception=id)
    except Exo.DoesNotExist:
        exoo = None
    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None
    return render(request, 'exo/exo.html', {'form': form, 'appointments': appointments, 'medicine': medicine, 'exoo': exoo, 'id': id})


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


def medicine(request,id):
    if request.method == 'POST':
        form = MedicinForm(request.POST)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id  # Set the foreign key to the specified 'id'
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name  # Set the name from Reception model
            oral_surgery.phone = reception.phone  # Set the name from Reception model
            oral_surgery.gender = reception.gender  # Set the gender from Reception model
            oral_surgery.date_of_birth = reception.date_of_birth  # Set the gender from Reception model
            oral_surgery.save()
            return redirect('all-medicine')
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = MedicinForm(initial=initial_data)  # Prepopulate the form with initial data

    appointments = Reception.objects.all().order_by('-id')


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
        orals = Reception.objects.filter(name__icontains=searched)
        receptions = Reception.objects.all()
        return render(request, 'exo/search_exo.html', {'searched': searched, 'orals': orals, 'receptions': receptions})
    else:
        return render(request, 'exo/search_exo.html', {})


def delete_exo(request, id):
    orals = Exo.objects.get(pk=id)
    orals.delete()
    return redirect('all-oral-surgery')
