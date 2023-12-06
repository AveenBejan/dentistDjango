# Generated by Django 4.2.1 on 2023-12-06 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0052_rename_components_first_endo_access_opiningt_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='endo',
            old_name='access_opiningt',
            new_name='components_first',
        ),
        migrations.RemoveField(
            model_name='endo',
            name='instrumentation',
        ),
        migrations.RemoveField(
            model_name='endo',
            name='opturation',
        ),
        migrations.AddField(
            model_name='endo',
            name='no_prepare',
            field=models.IntegerField(blank=True, null=True, verbose_name='no_prepare'),
        ),
    ]