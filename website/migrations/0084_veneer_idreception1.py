# Generated by Django 4.2.1 on 2024-02-29 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0083_crown_idreception1'),
    ]

    operations = [
        migrations.AddField(
            model_name='veneer',
            name='idReception1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception1'),
        ),
    ]
