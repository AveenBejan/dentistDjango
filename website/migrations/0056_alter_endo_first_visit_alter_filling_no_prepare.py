# Generated by Django 4.2.1 on 2023-12-09 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0055_alter_endo_first_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endo',
            name='first_visit',
            field=models.DateField(blank=True, max_length=20, null=True, verbose_name='date_of_birth'),
        ),
        migrations.AlterField(
            model_name='filling',
            name='no_prepare',
            field=models.IntegerField(blank=True, null=True, verbose_name='no_prepare'),
        ),
    ]
