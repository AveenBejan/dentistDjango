# Generated by Django 4.2.1 on 2023-07-19 11:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_rename_exo_image_exo_exo_images_alter_exo_regdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exo',
            name='exo_images',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='exo',
            name='regdate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Regdate'),
        ),
        migrations.AlterField(
            model_name='medicin',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 11, 1, 56, 244599), editable=False, verbose_name='Regdate'),
        ),
        migrations.AlterField(
            model_name='oralsurgery',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 11, 1, 56, 244599), editable=False, verbose_name='Regdate'),
        ),
        migrations.AlterField(
            model_name='reception',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 11, 1, 56, 241609), editable=False, verbose_name='Regdate'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/')),
                ('exo_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.exo')),
            ],
        ),
    ]
