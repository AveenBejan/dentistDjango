# Generated by Django 4.2.1 on 2023-10-29 13:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_alter_endo_fourth_visit_alter_endo_second_visit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exo',
            name='no_prepare',
        ),
        migrations.RemoveField(
            model_name='exo',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='oralsurgery',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 13, 5, 40, 989366), editable=False, verbose_name='Regdate'),
        ),
    ]
