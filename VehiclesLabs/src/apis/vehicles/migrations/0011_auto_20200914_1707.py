# Generated by Django 3.1 on 2020-09-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0010_auto_20200914_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclesdetail',
            name='fuelIndicator',
            field=models.FloatField(blank=True, max_length=15, null=True),
        ),
    ]
