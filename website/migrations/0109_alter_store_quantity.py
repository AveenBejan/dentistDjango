# Generated by Django 4.2.1 on 2024-07-02 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0108_rename_quantity_store_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
