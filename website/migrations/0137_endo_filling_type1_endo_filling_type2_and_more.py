# Generated by Django 4.2.1 on 2024-08-13 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0136_preventive_paymenthistory_preventive_instance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='endo',
            name='filling_type1',
            field=models.CharField(blank=True, max_length=120, verbose_name='filling_type'),
        ),
        migrations.AddField(
            model_name='endo',
            name='filling_type2',
            field=models.CharField(blank=True, max_length=120, verbose_name='filling_type'),
        ),
        migrations.AddField(
            model_name='endo',
            name='filling_type3',
            field=models.CharField(blank=True, max_length=120, verbose_name='filling_type'),
        ),
    ]
