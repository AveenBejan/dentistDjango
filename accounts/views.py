from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Assuming you have a custom form for user creation
from django.contrib.auth import login as auth_login

# Create your views here.


def signup(request):
    form = CustomUserCreationForm()  # Use your custom form here
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    return render(request, 'accounts/signup.html', {'form': form})


