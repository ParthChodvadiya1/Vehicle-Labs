# Generated by Django 3.1 on 2020-09-04 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_vehiclesdetail_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclesdetail',
            name='kilometer',
            field=models.FloatField(max_length=10, null=True),
        ),
    ]
