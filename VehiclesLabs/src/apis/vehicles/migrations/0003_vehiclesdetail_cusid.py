# Generated by Django 3.1 on 2020-08-28 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20200827_1733'),
        ('vehicles', '0002_auto_20200828_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclesdetail',
            name='cusID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customerdetail'),
        ),
    ]