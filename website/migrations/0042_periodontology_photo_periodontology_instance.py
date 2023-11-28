# Generated by Django 4.2.1 on 2023-11-26 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0041_alter_ortho_visit_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodontology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('phone', models.CharField(max_length=120, verbose_name='Phone')),
                ('gender', models.CharField(max_length=20, verbose_name='Gender')),
                ('date_of_birth', models.CharField(max_length=20, verbose_name='Gender')),
                ('type', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='price')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='price')),
                ('paid', models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='paid')),
                ('note', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='Regdate')),
                ('exo_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctors')),
                ('educational', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.educational')),
                ('idReception', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.reception')),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='periodontology_instance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.periodontology'),
        ),
    ]
