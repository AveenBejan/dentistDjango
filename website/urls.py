
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact.html', views.contact, name='contact'),
    path('about.html', views.about, name='about'),
    path('services.html', views.services, name='services'),
    path('doctors.html', views.doctors, name='doctors'),
    path('exo_reception.html', views.reception, name='reception'),
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

    path('exo/<int:id>',views.exo, name='exo'),
    path('exo/exo_reception.html',views.exo_reception, name='exo-reception'),
    path('exo/all_exo.html',views.all_exo, name='all-exo'),
    path('search_exo', views.search_exo, name='search-exo'),
    path('search_exo1', views.search_exo1, name='search-exo1'),
    path('exo/exo_reception1.html',views.exo_reception1, name='exo-reception1'),
    path('delete_exo/<int:id>', views.delete_exo, name='delete-exo'),


    path('medicine/<int:id>',views.medicine, name='medicine'),
    path('exo/all_medicine.html',views.all_medicine, name='all-medicine'),
    path('print_medicine/<int:id>',views.print_medicine, name='print-medicine'),
    path('print_medicine1/<int:id>',views.print_medicine1, name='print-medicine1'),
    path('drugs/medicine1.html', views.medicine1, name='medicine1'),
    path('delete-medicine1/<int:id>', views.delete_medicine1, name='delete-medicine1'),

    path('drugs/<int:id>/', views.drugs, name='drugs'),
    path('print_drugs/<int:id>', views.print_drugs, name='print-drugs'),



    path('conservation/crown/crown_reception.html',views.crown_reception, name='crown-reception'),
    path('search_crown', views.search_crown, name='search-crown'),
    path('crown/<int:id>',views.crown, name='crown'),

    path('conservation/veneer/veneer_reception.html', views.veneer_reception, name='veneer-reception'),
    path('search_veneer', views.search_veneer, name='search-veneer'),
    path('veneer/<int:id>', views.veneer, name='veneer'),

    path('filling/<int:id>', views.filling, name='filling'),
    path('filling/filling_reception.html', views.filling_reception, name='filling-reception'),
    path('search_filling', views.search_filling, name='search-filling'),

    path('search_appo', views.search_appo, name='search-appo'),
    path('appointment1.html', views.appointment1, name='appointment1'),
    path('all_appo.html', views.all_appo, name='all-appo'),
    path('dentist-details/<int:id>', views.dentist_details, name='dentist-details'),
    path('all_details.html', views.all_details, name='all-details'),
    path('update/<int:id>', views.update, name='update'),
    path('delete_details/<int:id>', views.delete_details, name='delete-details'),
    path('search_details',views.search_details,name='search-details'),



]
