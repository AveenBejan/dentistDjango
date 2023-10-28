# Generated by Django 4.2.1 on 2023-10-27 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_endo_canal_endo_work_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endo',
            name='fourth_visit',
            field=models.CharField(max_length=20, null=True, verbose_name='date_of_birth'),
        ),
        migrations.AlterField(
            model_name='endo',
            name='second_visit',
            field=models.CharField(max_length=20, null=True, verbose_name='date_of_birth'),
        ),
        migrations.AlterField(
            model_name='endo',
            name='third_visit',
            field=models.CharField(max_length=20, null=True, verbose_name='date_of_birth'),
        ),
        migrations.AlterField(
            model_name='oralsurgery',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 27, 20, 17, 45, 64352), editable=False, verbose_name='Regdate'),
        ),
    ]
