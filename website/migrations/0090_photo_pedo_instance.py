# Generated by Django 4.2.1 on 2024-06-23 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0089_pedo'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='pedo_instance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.pedo'),
        ),
    ]
