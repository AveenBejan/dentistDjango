# Generated by Django 4.2.1 on 2023-11-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0038_ortho_brackets'),
    ]

    operations = [
        migrations.AddField(
            model_name='ortho',
            name='regdatev',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Regdatev'),
        ),
    ]