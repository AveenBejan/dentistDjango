# Generated by Django 4.2.1 on 2024-07-02 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0105_endo_filling_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_name', models.CharField(max_length=120, verbose_name='lab_name')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
            ],
        ),
    ]
