# Generated by Django 4.2.1 on 2023-08-09 15:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('gender', models.CharField(max_length=50, verbose_name='Gender')),
                ('birthday', models.DateTimeField()),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('address', models.CharField(max_length=300, verbose_name='Address')),
                ('date', models.DateTimeField()),
                ('phone', models.CharField(max_length=20, verbose_name='Phone')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('subject', models.CharField(max_length=300, verbose_name='Address')),
                ('message', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Crown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='Phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.CharField(max_length=20, verbose_name='Gender')),
                ('shade', models.CharField(blank=True, max_length=120, verbose_name='shade')),
                ('no_unite', models.CharField(blank=True, max_length=120, verbose_name='no_unite')),
                ('color', models.CharField(blank=True, max_length=120, verbose_name='color')),
                ('no_prepare', models.IntegerField(blank=True, verbose_name='no_prepare')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='price')),
                ('note', models.CharField(blank=True, max_length=120, null=True, verbose_name='note')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('exo_images', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
            ],
        ),
        migrations.CreateModel(
            name='Exo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='Phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.CharField(max_length=20, verbose_name='Gender')),
                ('ur', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('ul', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('lr', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('ll', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('no_prepare', models.IntegerField(blank=True, null=True, verbose_name='no_prepare')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='price')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='total_price')),
                ('note', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('exoby', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('simpleexo', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('complcated', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('exo_images', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Filling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='Phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.CharField(max_length=20, verbose_name='date_of_birth')),
                ('filling_type', models.CharField(blank=True, max_length=120, verbose_name='filling_type')),
                ('filling_place', models.CharField(blank=True, max_length=120, verbose_name='filling_place')),
                ('ur', models.CharField(blank=True, max_length=120, null=True, verbose_name='ur')),
                ('ul', models.CharField(blank=True, max_length=120, null=True, verbose_name='ul')),
                ('lr', models.CharField(blank=True, max_length=120, null=True, verbose_name='lr')),
                ('ll', models.CharField(blank=True, max_length=120, null=True, verbose_name='ll')),
                ('no_prepare', models.IntegerField(verbose_name='no_prepare')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='price')),
                ('note', models.CharField(blank=True, max_length=120, null=True, verbose_name='note')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('exo_images', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_medicine', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Orthodontics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('yes_no_field', models.CharField(max_length=100)),
                ('material_field', models.CharField(max_length=100)),
                ('width_field', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.DateField()),
                ('time', models.CharField(max_length=200, null=True)),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors')),
            ],
        ),
        migrations.CreateModel(
            name='Veneer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='Phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.CharField(max_length=20, verbose_name='Gender')),
                ('shade', models.CharField(blank=True, max_length=120, verbose_name='shade')),
                ('no_unite', models.CharField(blank=True, max_length=120, verbose_name='no_unite')),
                ('color', models.CharField(blank=True, max_length=120, verbose_name='color')),
                ('no_prepare', models.IntegerField(blank=True, verbose_name='no_prepare')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='price')),
                ('note', models.CharField(blank=True, max_length=120, null=True, verbose_name='note')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('exo_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('idReception', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/')),
                ('crown_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.crown')),
                ('exo_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.exo')),
                ('filling_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.filling')),
                ('veneer_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.veneer')),
            ],
        ),
        migrations.CreateModel(
            name='OralSurgery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tooth', models.CharField(max_length=120, verbose_name='tooth')),
                ('RX', models.CharField(blank=True, max_length=120, verbose_name='RX')),
                ('material_type', models.CharField(blank=True, max_length=120, verbose_name='material_type')),
                ('thickness_rich', models.CharField(blank=True, max_length=120, verbose_name='thickness_rich')),
                ('size', models.CharField(blank=True, max_length=120, verbose_name='size')),
                ('size_direction', models.CharField(blank=True, max_length=120, verbose_name='size_direction')),
                ('size_number', models.CharField(blank=True, max_length=120, verbose_name='size_number')),
                ('second_visit', models.CharField(blank=True, max_length=120, verbose_name='second_visit')),
                ('third_visit', models.CharField(blank=True, max_length=120, verbose_name='third_visit')),
                ('fourth_visit', models.CharField(blank=True, max_length=120, verbose_name='fourth_visit')),
                ('fifth_visit', models.CharField(blank=True, max_length=120, verbose_name='fifth_visit')),
                ('regdate', models.DateTimeField(default=datetime.datetime(2023, 8, 9, 15, 4, 54, 26319), editable=False, verbose_name='Regdate')),
                ('idReception', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception')),
            ],
        ),
        migrations.CreateModel(
            name='Medicin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='Phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.CharField(max_length=20, verbose_name='Gender')),
                ('antibiotic', models.CharField(blank=True, max_length=120, verbose_name='antibiotic')),
                ('analogous', models.CharField(blank=True, max_length=120, verbose_name='analogous')),
                ('mouthwash', models.CharField(blank=True, max_length=120, verbose_name='mouthwash')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('idReception', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception')),
            ],
        ),
        migrations.AddField(
            model_name='filling',
            name='idReception',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception'),
        ),
        migrations.AddField(
            model_name='exo',
            name='idReception',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception'),
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_medicine', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(blank=True, max_length=120, verbose_name='Name')),
                ('phone', models.CharField(blank=True, max_length=120, verbose_name='Phone')),
                ('gender', models.CharField(blank=True, max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.CharField(blank=True, max_length=20, verbose_name='Gender')),
                ('doze', models.CharField(blank=True, max_length=200)),
                ('type', models.CharField(blank=True, max_length=200)),
                ('times', models.CharField(blank=True, max_length=200)),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('idReception', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception')),
            ],
        ),
        migrations.CreateModel(
            name='DentistDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(max_length=200, verbose_name='Details')),
                ('medicine_name', models.CharField(max_length=300, verbose_name='Medicine Name')),
                ('medicine_time', models.CharField(max_length=50, verbose_name='Medicine Time')),
                ('medicine_period', models.CharField(max_length=50, verbose_name='Medicine Period')),
                ('medicine_tfood', models.CharField(max_length=50, verbose_name='Medicine T-Food')),
                ('medicine_no', models.CharField(max_length=20, verbose_name='Medicine No')),
                ('idappointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.appointment1')),
            ],
        ),
        migrations.AddField(
            model_name='crown',
            name='idReception',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception'),
        ),
    ]
