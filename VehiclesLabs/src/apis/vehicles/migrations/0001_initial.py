# Generated by Django 3.1 on 2020-08-27 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VehiclesDetail',
            fields=[
                ('vehicleID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('vehiclenumber', models.CharField(max_length=10)),
                ('kilometer', models.FloatField(max_length=10)),
                ('chasisnumber', models.CharField(max_length=17, null=True)),
                ('enginenumber', models.CharField(max_length=17, null=True)),
                ('fuelIndicator', models.FloatField(null=True)),
                ('userID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]