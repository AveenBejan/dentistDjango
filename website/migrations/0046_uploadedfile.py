# Generated by Django 4.2.1 on 2023-11-28 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0045_alter_drug_dispense_alter_drug_doze_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
            ],
        ),
    ]
