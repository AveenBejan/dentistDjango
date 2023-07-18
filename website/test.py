def exo(request, id):
    if request.method == 'POST':
        form = ExoForm(request.POST, request.FILES)
        if form.is_valid():
            oral_surgery = form.save(commit=False)
            oral_surgery.idReception_id = id  # Set the foreign key to the specified 'id'
            reception = Reception.objects.get(id=id)
            oral_surgery.name = reception.name  # Set the name from Reception model
            oral_surgery.phone = reception.phone  # Set the name from Reception model
            oral_surgery.gender = reception.gender  # Set the gender from Reception model
            oral_surgery.date_of_birth = reception.date_of_birth  # Set the gender from Reception model
            oral_surgery.save()

            # Get the list of uploaded files
            files = request.FILES.getlist('exo_image')

            # Loop through each uploaded file
            for file in files:
                exo_image = Exo(exo_image=file)
                exo_image.save()

            return redirect('exo', id=id)
    else:
        reception = Reception.objects.get(id=id)
        initial_data = {
            'idReception': id,
            'name': reception.name,
            'phone': reception.phone,
            'gender': reception.gender,
            'date_of_birth': reception.date_of_birth
        }
        form = ExoForm(initial=initial_data)  # Prepopulate the form with initial data

    appointments = Reception.objects.all().order_by('-id')
    try:
        exoo = Exo.objects.get(idReception=id)
    except Exo.DoesNotExist:
        exoo = None
    try:
        medicine = Medicin.objects.get(idReception=id)
    except Medicin.DoesNotExist:
        medicine = None
    return render(request, 'exo/exo.html', {'form': form, 'appointments': appointments, 'medicine': medicine, 'exoo': exoo, 'id': id})