from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Assuming you have a custom form for user creation
from django.contrib.auth import login as auth_login
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.


def signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'You have been successfully logged in.')
            return redirect('login')  # Redirect to the login page
    return render(request, 'accounts/signup.html', {'form': form})


def my_login_view(request):
    # Your login logic here...
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        auth_login(request, user)
        messages.success(request, 'You have successfully logged in.')
        return redirect('home')  # Redirect to the home page after login
    else:
        messages.error(request, 'Invalid username or password.')
        return redirect('login')  # Redirect back to the login page with an error message


def all_customer(request):
    appointments = CustomUser.objects.all().order_by('-id')
    return render(request, 'accounts/all_customer.html', {'appointments': appointments})


