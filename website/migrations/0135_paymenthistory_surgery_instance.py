# Generated by Django 4.2.1 on 2024-07-26 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0134_surgery_photo_surgery_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='surgery_instance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.surgery'),
        ),
    ]
