# Generated by Django 4.2.1 on 2023-11-24 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0034_drug_tablet'),
    ]

    operations = [
        migrations.AddField(
            model_name='exo',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AddField(
            model_name='ortho',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='price'),
        ),
    ]