# Generated by Django 4.2.1 on 2024-07-02 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0104_alter_doctors_proportion_center_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='endo',
            name='filling_type',
            field=models.CharField(blank=True, max_length=120, verbose_name='filling_type'),
        ),
    ]
