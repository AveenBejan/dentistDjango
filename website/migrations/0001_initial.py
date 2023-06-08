# Generated by Django 4.2.1 on 2023-06-08 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
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
    ]
