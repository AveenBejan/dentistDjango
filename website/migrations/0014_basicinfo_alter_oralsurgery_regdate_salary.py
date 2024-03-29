# Generated by Django 4.2.1 on 2023-09-08 00:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_crown_paid_filling_paid_oralsurgery_paid_veneer_paid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=120, verbose_name='fullname')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('phoneNumber', models.CharField(max_length=120, verbose_name='phoneNumber')),
                ('address', models.CharField(max_length=120, verbose_name='address')),
                ('type', models.CharField(max_length=120, verbose_name='type')),
                ('startDay', models.DateField()),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
            ],
        ),
        migrations.AlterField(
            model_name='oralsurgery',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 0, 29, 1, 601908), editable=False, verbose_name='Regdate'),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=120, verbose_name='fullname')),
                ('salaryPaid', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='salaryPaid')),
                ('days', models.IntegerField(verbose_name='days')),
                ('finalSalary', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='finalSalary')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('idBasicInfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.basicinfo')),
            ],
        ),
    ]
