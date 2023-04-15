# Generated by Django 3.1 on 2020-12-21 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiclebrands', '0004_auto_20200910_1608'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='vehiclebrand',
            index=models.Index(fields=['brandname', 'brandmodel', '-createdAt'], name='vehiclebran_brandna_aaebb0_idx'),
        ),
    ]
