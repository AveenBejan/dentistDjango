# Generated by Django 4.2.1 on 2023-11-26 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0043_prosthodontics_photo_prosthodontics_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='dispense',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
