# Generated by Django 3.1 on 2020-09-14 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0009_auto_20200910_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclesdetail',
            name='fuelIndicator',
            field=models.FloatField(null=True),
        ),
    ]
