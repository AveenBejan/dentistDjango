# Generated by Django 4.2.1 on 2023-12-28 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0069_paymenthistory_prosthodontics_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='exo_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.exo'),
        ),
    ]
