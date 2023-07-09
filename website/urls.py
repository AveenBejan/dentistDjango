
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact.html', views.contact, name='contact'),
    path('about.html', views.about, name='about'),
    path('services.html', views.services, name='services'),
    path('doctors.html', views.doctors, name='doctors'),
    path('reception.html', views.reception, name='reception'),
    path('all_reception.html', views.all_reception, name='all-reception'),
    path('oral_reception.html', views.oral_reception, name='oral-reception'),
    path('delete_reception/<int:id>', views.delete_reception, name='delete-reception'),
    path('update_reception/<int:id>', views.update_reception, name='update-reception'),
    path('add-oral-surgery/<int:id>', views.add_oral_surgery, name='add-oral-surgery'),
    path('index.html', views.add_oral_surgery, name='add-oral-surgery'),
    path('search_oral_surgery', views.search_oral_surgery, name='search-oral-surgery'),
    path('updateee_oral_surgery/<int:id>', views.updateee_oral_surgery, name='updateee-oral-surgery'),
    path('delete_orla_surgery/<int:id>', views.delete_orla_surgery, name='delete-orla-surgery'),
    path('all_oral_surgery.html', views.all_oral_surgery, name='all-oral-surgery'),
    path('orthodontic.html', views.orthodontics, name='orthodontics'),


    path('search_appo', views.search_appo, name='search-appo'),
    path('appointment1.html', views.appointment1, name='appointment1'),
    path('all_appo.html', views.all_appo, name='all-appo'),
    path('dentist-details/<int:id>', views.dentist_details, name='dentist-details'),
    path('all_details.html', views.all_details, name='all-details'),
    path('update/<int:id>', views.update, name='update'),
    path('delete_details/<int:id>', views.delete_details, name='delete-details'),
    path('search_details',views.search_details,name='search-details'),



]
