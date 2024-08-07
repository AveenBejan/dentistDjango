# Generated by Django 4.2.1 on 2024-06-28 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0096_alter_doctors_proportion_center_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='proportion_center',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=8, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='proportion_doctor',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=8, null=True, verbose_name='price'),
        ),
    ]
