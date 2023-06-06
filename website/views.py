from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'home.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        #send email to manager
        send_mail(subject,message,email,['aabduljabar@swedoaid.org']
          )
        return render(request, 'contact.html',{'name':name})
    else:
        return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def doctors(request):
    return render(request, 'doctors.html')


def appointment(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        Date = request.POST['Date']
        Time = request.POST['Time']
        phone = request.POST['phone']

        # send email to manager
        appointment = "Name: " + name +"<br/>"+\
                      "Email: " + email +"<br/>"+\
                      "address: " +address +"<br/>"+\
                      "Date: " +Date +"<br/>"+\
                      "Time: " + Time +"<br/>"+\
                      "phone: " + phone

        send_mail('Appointment Request',appointment,email,['aabduljabar@swedoaid.org'])

        return render(request, 'appointment.html',{
            'name':  name,
            'email': email,
            'address': address,
            'Date': Date,
            'Time': Time,
            'phone': phone
        })
    else:
        return render(request, 'home.html')
