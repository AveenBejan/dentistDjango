# Generated by Django 4.2.1 on 2023-11-26 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0040_remove_ortho_regdatev_ortho_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ortho',
            name='visit_date',
            field=models.DateField(blank=True, null=True, verbose_name='Visit Date'),
        ),
    ]
