# Generated by Django 4.2.1 on 2023-08-25 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_alter_oralsurgery_regdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oralsurgery',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 25, 20, 36, 12, 44298), editable=False, verbose_name='Regdate'),
        ),
    ]
