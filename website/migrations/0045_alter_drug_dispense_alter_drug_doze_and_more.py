# Generated by Django 4.2.1 on 2023-11-27 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0044_drug_dispense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='dispense',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='doze',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='tablet',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='times',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]