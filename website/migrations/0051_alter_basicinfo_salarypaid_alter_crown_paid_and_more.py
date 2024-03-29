# Generated by Django 4.2.1 on 2023-12-06 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0050_alter_ortho_price_alter_ortho_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='salaryPaid',
            field=models.DecimalField(decimal_places=0, max_digits=8, null=True, verbose_name='salaryPaid'),
        ),
        migrations.AlterField(
            model_name='crown',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='crown',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=8, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='crown',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='debts',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='debts',
            name='remaining',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='remaining'),
        ),
        migrations.AlterField(
            model_name='debts',
            name='totalPrice',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='totalPrice'),
        ),
        migrations.AlterField(
            model_name='endo',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='endo',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=8, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='endo',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='exo',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='exo',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='exo',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='filling',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='filling',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=8, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='filling',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='oralsurgery',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='oralsurgery',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=8, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='oralsurgery',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='ortho',
            name='paid',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=8, verbose_name='finalSalary'),
        ),
        migrations.AlterField(
            model_name='periodontology',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='periodontology',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='periodontology',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='prosthodontics',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='prosthodontics',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='prosthodontics',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='finalSalary',
            field=models.DecimalField(decimal_places=0, max_digits=8, verbose_name='finalSalary'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='salaryPaid',
            field=models.DecimalField(decimal_places=0, max_digits=8, verbose_name='salaryPaid'),
        ),
        migrations.AlterField(
            model_name='veneer',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='paid'),
        ),
        migrations.AlterField(
            model_name='veneer',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=8, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='veneer',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=20, verbose_name='price'),
        ),
    ]
