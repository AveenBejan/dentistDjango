# Generated by Django 4.2.1 on 2023-11-22 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0033_educational_reception_educational'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='tablet',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]