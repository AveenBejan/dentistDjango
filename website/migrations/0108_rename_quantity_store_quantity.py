# Generated by Django 4.2.1 on 2024-07-02 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0107_materialoutput'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='Quantity',
            new_name='quantity',
        ),
    ]
