
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.reception, name='home'),
    path('gave_appointment/<int:id>', views.gave_appointment, name='gave-appointment'),
    path('print_appointment/<int:id>', views.print_appointment, name='print-appointment'),
    path('all_gave.html', views.all_gave, name='all-gave'),
    path('contact.html', views.contact, name='contact'),
    path('about.html', views.about, name='about'),
    path('services.html', views.services, name='services'),
    path('doctors.html', views.doctors, name='doctors'),
    path('exo_reception.html', views.reception, name='reception'),
    path('all-reception', views.all_reception, name='all-reception'),

    path('user_all', views.user_all, name='user_all'),
    path('custom_login', views.custom_login, name='custom_login'),
    path('update_appointment/<int:id>/', views.update_appointment, name='update_appointment'),

    path('oral_reception.html', views.oral_reception, name='oral-reception'),
    path('delete_reception/<int:id>', views.delete_reception, name='delete-reception'),
    path('search_reception', views.search_reception, name='search-reception'),
    path('update-reception/<int:id>', views.update_reception, name='update-reception'),
    path('add-oral-surgery/<int:id>', views.add_oral_surgery, name='add-oral-surgery'),
    path('index.html', views.add_oral_surgery, name='add-oral-surgery'),
    path('search_oral', views.search_oral, name='search-oral'),
    path('oral_edit/<int:id>', views.oral_edit, name='oral-edit'),
    path('oral_visit/<int:id>', views.oral_visit, name='oral-visit'),
    path('delete_oral/<int:id>', views.delete_oral, name='delete-oral'),
    path('all_oral_surgery.html', views.all_oral_surgery, name='all-oral-surgery'),
    path('remove_photo_oral/<int:photo_id>/', views.remove_photo_oral, name='remove-photo-oral'),
    path('implant.html', views.implant, name='implant'),
    path('delete-implant/<int:id>', views.delete_implant, name='delete-implant'),
    path('send_appointment_reminders', views.send_appointment_reminders, name='send_appointment_reminders'),
    path('generate_pdf/', views.generate_pdf_view, name='generate_pdf'),

    path('upload/', views.upload_file, name='upload'),
    path('delete_upload_file/<int:id>', views.delete_upload_file, name='delete-upload_file'),

    path('doctors/doctor.html', views.doctor, name='doctor'),
    path('delete-doctor/<int:id>', views.delete_doctor, name='delete-doctor'),
    path('search_doctor', views.search_doctor, name='search-doctor'),

    path('educational/educational.html', views.educational, name='educational'),
    path('delete-educational/<int:id>', views.delete_educational, name='delete-educational'),
    path('search_educational', views.search_educational, name='search-educational'),
    path('search_education', views.search_education, name='search-education'),


    path('exo/<int:id>',views.exo, name='exo'),
    path('exo/exo_reception.html',views.exo_reception, name='exo-reception'),
    path('exo/all_exo.html',views.all_exo, name='all-exo'),
    path('exo_edit/<int:id>', views.exo_edit, name='exo_edit'),
    path('remove_photo/<int:photo_id>/', views.remove_photo, name='remove_photo'),
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
    path('delete_drugs/<int:id>', views.delete_drugs, name='delete-drugs'),



    path('conservation/crown/crown_reception.html',views.crown_reception, name='crown-reception'),
    path('search_crown', views.search_crown, name='search-crown'),
    path('crown/<int:id>',views.crown, name='crown'),
    path('crown_edit/<int:id>', views.crown_edit, name='crown_edit'),
    path('remove_photo_crown/<int:photo_id>/', views.remove_photo_crown, name='remove_photo_crown'),
    path('delete_crown/<int:id>', views.delete_crown, name='delete-crown'),
    path('crown_pdf', views.crown_pdf, name='crown-pdf'),


    path('periodontology/<int:id>',views.periodontology, name='periodontology'),
    path('periodontology/periodontology_reception.html', views.periodontology_reception, name='periodontology-reception'),
    path('periodontology_edit/<int:id>', views.periodontology_edit, name='periodontology_edit'),
    path('remove_photo_periodontology/<int:photo_id>/', views.remove_photo_periodontology, name='remove_photo_periodontology'),
    path('search_periodontology', views.search_periodontology, name='search-periodontology'),
    path('delete_periodontology/<int:id>', views.delete_periodontology, name='delete-periodontology'),


    path('prosthodontics/prosthodontics_reception.html', views.prosthodontics_reception,name='prosthodontics-reception'),
    path('search_prosthodontics', views.search_prosthodontics, name='search-prosthodontics'),
    path('prosthodontics/<int:id>', views.prosthodontics, name='prosthodontics'),
    path('prosthodontics_edit/<int:id>', views.prosthodontics_edit, name='prosthodontics_edit'),
    path('remove_photo_prosthodontics/<int:photo_id>/', views.remove_photo_prosthodontics, name='remove_photo_prosthodontics'),
    path('delete_prosthodontics/<int:id>', views.delete_prosthodontics, name='delete-prosthodontics'),


    path('conservation/veneer/veneer_reception.html', views.veneer_reception, name='veneer-reception'),
    path('search_veneer', views.search_veneer, name='search-veneer'),
    path('veneer/<int:id>', views.veneer, name='veneer'),
    path('veneer_edit/<int:id>', views.veneer_edit, name='veneer_edit'),
    path('remove_photo_veneer/<int:photo_id>/', views.remove_photo_veneer, name='remove_photo_veneer'),
    path('delete_veneer/<int:id>', views.delete_veneer, name='delete-veneer'),


    path('filling/<int:id>', views.filling, name='filling'),
    path('filling/filling_reception.html', views.filling_reception, name='filling-reception'),
    path('search_filling', views.search_filling, name='search-filling'),
    path('filling_edit/<int:id>', views.filling_edit, name='filling_edit'),
    path('remove_photo_filling/<int:photo_id>/', views.remove_photo_filling, name='remove_photo_filling'),
    path('delete_filling/<int:id>', views.delete_filling, name='delete-filling'),

    path('add-endo/<int:id>', views.add_endo, name='add-endo'),
    path('conservation/endo/endo_reception.html', views.endo_reception, name='endo-reception'),
    path('conservation/endo/endo.html', views.add_endo, name='add-endo'),
    path('endo_edit/<int:id>', views.endo_edit, name='endo-edit'),
    path('search_endo', views.search_endo, name='search-endo'),
    path('endo_visit/<int:id>', views.endo_visit, name='endo-visit'),
    path('delete_endo/<int:id>', views.delete_endo, name='delete-endo'),
    path('remove_photo_endo/<int:photo_id>/', views.remove_photo_endo, name='remove-photo-endo'),

    path('add-ortho/<int:id>', views.add_ortho, name='add-ortho'),
    path('ortho/ortho_reception.html', views.ortho_reception, name='ortho-reception'),
    path('ortho/ortho.html', views.add_ortho, name='add-ortho'),
    path('ortho_edit/<int:id>', views.ortho_edit, name='ortho-edit'),
    path('search_ortho', views.search_ortho, name='search-ortho'),
    path('ortho_visit/<int:id>', views.ortho_visit, name='ortho-visit'),
    path('ortho_visit1/<int:id>', views.ortho_visit1, name='ortho-visit1'),
    path('start_ortho/<int:id>', views.start_ortho, name='start-ortho'),
    path('delete_ortho/<int:idReception_id>', views.delete_ortho, name='delete-ortho' ),
    path('remove_photo_ortho/<int:photo_id>/', views.remove_photo_ortho, name='remove-photo-ortho'),
    path('visit.html', views.visit, name='visit'),
    path('delete_visit/<int:id>', views.delete_visit, name='delete-visit'),


    path('search_appo', views.search_appo, name='search-appo'),
    path('appointment1.html', views.appointment1, name='appointment1'),
    path('all_appo.html', views.all_appo, name='all-appo'),
    path('dentist-details/<int:id>', views.dentist_details, name='dentist-details'),
    path('all_details.html', views.all_details, name='all-details'),
    path('update/<int:id>', views.update, name='update'),
    path('delete_details/<int:id>', views.delete_details, name='delete-details'),
    path('search_details',views.search_details,name='search-details'),

    path('search/', views.search_view, name='search'),

    path('search_debts', views.search_debts, name='search-debts'),
    path('search_debts1', views.search_debts1, name='search-debts1'),
    path('search_educational1', views.search_educational1, name='search-educational1'),
    path('print_exo_debt/<int:id>', views.print_exo_debt, name='print_exo_debt'),
    path('print_crown_debt/<int:id>', views.print_crown_debt, name='print_crown_debt'),
    path('print_filling_debt/<int:id>', views.print_filling_debt, name='print_filling_debt'),
    path('print_veneer_debt/<int:id>', views.print_veneer_debt, name='print_veneer_debt'),
    path('print_oral_debt/<int:id>', views.print_oral_debt, name='print_oral_debt'),
    path('print_endo_debt/<int:id>', views.print_endo_debt, name='print_endo_debt'),
    path('print_ortho_debt/<int:id>', views.print_ortho_debt, name='print_ortho_debt'),
    path('print_periodontology_debt/<int:id>', views.print_periodontology_debt, name='print_periodontology_debt'),
    path('print_prosthodontics_debt/<int:id>', views.print_prosthodontics_debt, name='print_prosthodontics_debt'),



    path('add_debt/<int:id>', views.add_debt, name='add-debt'),
    path('add_debt_crown/<int:id>', views.add_debt_crown, name='add-debt-crown'),
    path('add_debt_filling/<int:id>', views.add_debt_filling, name='add-debt-filling'),
    path('add_debt_veneer/<int:id>', views.add_debt_veneer, name='add-debt-veneer'),
    path('add_debt_oral/<int:id>', views.add_debt_oral, name='add-debt-oral'),
    path('add_debt_endo/<int:id>', views.add_debt_endo, name='add-debt-endo'),
    path('add_debt_ortho/<int:id>', views.add_debt_ortho, name='add-debt-ortho'),
    path('add_debt1/<int:id>', views.add_debt1, name='add-debt1'),
    path('add_debt_crown1/<int:id>', views.add_debt_crown1, name='add-debt-crown1'),
    path('add_debt_filling1/<int:id>', views.add_debt_filling1, name='add-debt-filling1'),
    path('add_debt_veneer1/<int:id>', views.add_debt_veneer1, name='add-debt-veneer1'),
    path('add_debt_oral1/<int:id>', views.add_debt_oral1, name='add-debt-oral1'),
    path('add_debt_endo1/<int:id>', views.add_debt_endo1, name='add-debt-endo1'),
    path('add_debt_ortho1/<int:id>', views.add_debt_ortho1, name='add-debt-ortho1'),
    path('add_debt_periodontology1/<int:id>', views.add_debt_periodontology1, name='add-debt-periodontology1'),
    path('add_debt_periodontology/<int:id>', views.add_debt_periodontology, name='add-debt-periodontology'),
    path('add_debt_prosthodontics1/<int:id>', views.add_debt_prosthodontics1, name='add-debt-prosthodontics1'),
    path('add_debt_prosthodontics/<int:id>', views.add_debt_prosthodontics, name='add-debt-prosthodontics'),

    path('all_debts', views.all_debts, name='all_debts'),
    path('all_debts1', views.all_debts1, name='all_debts1'),
    path('add_new_employ', views.add_new_employ, name='add-new-employ'),
    path('delete_employ/<int:id>', views.delete_employ, name='delete-employ'),
    path('add_salary/<int:id>', views.add_salary, name='add-salary'),
    path('salary_reception', views.salary_reception, name='salary_reception'),
    path('update_employ/<int:id>', views.update_employ, name='update-employ'),


    path('add_outcome', views.add_outcome, name='add-outcome'),
    path('delete_outcome/<int:id>', views.delete_outcome, name='delete-outcome'),
    path('search_debts_history', views.search_debts_history, name='search-debts-history'),

    path('all_total', views.all_total, name='all-total'),
    path('feedback_view', views.feedback_view, name='feedback_view'),




]
