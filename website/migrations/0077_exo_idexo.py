# Generated by Django 4.2.1 on 2024-02-26 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0076_reception1'),
    ]

    operations = [
        migrations.AddField(
            model_name='exo',
            name='idExo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception1'),
        ),
    ]
