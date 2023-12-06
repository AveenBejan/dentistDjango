# Generated by Django 4.2.1 on 2023-12-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0051_alter_basicinfo_salarypaid_alter_crown_paid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='endo',
            old_name='components_first',
            new_name='access_opiningt',
        ),
        migrations.RemoveField(
            model_name='endo',
            name='no_prepare',
        ),
        migrations.AddField(
            model_name='endo',
            name='instrumentation',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='components'),
        ),
        migrations.AddField(
            model_name='endo',
            name='opturation',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='components'),
        ),
    ]
