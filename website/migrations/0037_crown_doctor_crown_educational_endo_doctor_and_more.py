# Generated by Django 4.2.1 on 2023-11-25 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0036_exo_educational'),
    ]

    operations = [
        migrations.AddField(
            model_name='crown',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors'),
        ),
        migrations.AddField(
            model_name='crown',
            name='educational',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.educational'),
        ),
        migrations.AddField(
            model_name='endo',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors'),
        ),
        migrations.AddField(
            model_name='endo',
            name='educational',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.educational'),
        ),
        migrations.AddField(
            model_name='exo',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors'),
        ),
        migrations.AddField(
            model_name='filling',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors'),
        ),
        migrations.AddField(
            model_name='filling',
            name='educational',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.educational'),
        ),
        migrations.AddField(
            model_name='oralsurgery',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors'),
        ),
        migrations.AddField(
            model_name='oralsurgery',
            name='educational',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.educational'),
        ),
        migrations.AddField(
            model_name='ortho',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors'),
        ),
        migrations.AddField(
            model_name='ortho',
            name='educational',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.educational'),
        ),
        migrations.AddField(
            model_name='veneer',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors'),
        ),
        migrations.AddField(
            model_name='veneer',
            name='educational',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.educational'),
        ),
    ]
