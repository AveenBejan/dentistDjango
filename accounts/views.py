from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Assuming you have a custom form for user creation
from django.contrib.auth import login as auth_login
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'

    def get_success_message(self, cleaned_data):
        return None

    def form_valid(self, form):
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)


def signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'You have been successfully  Registered and logged in.')
            return redirect('login')  # Redirect to the login page
    return render(request, 'accounts/signup.html', {'form': form})


def all_customer(request):
    appointments = CustomUser.objects.all().order_by('-id')
    return render(request, 'accounts/all_customer.html', {'appointments': appointments})


