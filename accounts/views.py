from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Assuming you have a custom form for user creation
from django.contrib.auth import login as auth_login
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

# Create your views here.


def signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    return render(request, 'accounts/signup.html', {'form': form})


def all_customer(request):
    appointments = CustomUser.objects.all().order_by('-id')
    return render(request, 'accounts/all_customer.html', {'appointments': appointments})


