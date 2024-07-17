# Generated by Django 4.2.1 on 2024-07-11 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0124_pedo_center_share_pedo_discount_option_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='veneer',
            name='center_share',
            field=models.DecimalField(decimal_places=0, max_digits=8, null=True, verbose_name='price'),
        ),
        migrations.AddField(
            model_name='veneer',
            name='discount_option',
            field=models.CharField(max_length=20, null=True, verbose_name='Gender'),
        ),
        migrations.AddField(
            model_name='veneer',
            name='doctor_share',
            field=models.DecimalField(decimal_places=0, max_digits=8, null=True, verbose_name='price'),
        ),
        migrations.AddField(
            model_name='veneer',
            name='lab_name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='veneer',
            name='price_lab',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True, verbose_name='price'),
        ),
    ]
