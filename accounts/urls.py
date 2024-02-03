from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('', views.CustomLoginView.as_view(), name='login'),  # Using CustomLoginView instead of auth_views.LoginView
    path('all_customer',views.all_customer,name='all_customer'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),






]