# Generated by Django 4.2.1 on 2024-01-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('doctor', 'Doctor'), ('user', 'User'), ('educational_center', 'Educational Center'), ('patient', 'Patient')], max_length=20),
        ),
    ]
