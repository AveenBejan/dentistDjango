from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, AppointmentForm


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
           send_mail(subject,message,email,['aabduljabar@swedoaid.org'])
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


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            date = form.cleaned_data['Date']
            time = form.cleaned_data['Time']
            phone = form.cleaned_data['phone']
            send_mail(name, email, address, date, time, name, phone, ['aabduljabar@swedoaid.org'])
            form.save()
            return render(request, 'appointmentt.html', {'form': form})
    else:
        form = AppointmentForm()
        return render(request, 'home.html')

