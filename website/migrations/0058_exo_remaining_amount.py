# Generated by Django 4.2.1 on 2023-12-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0057_remove_filling_filling_place_filling_fillingll1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exo',
            name='remaining_amount',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
    ]