# Generated by Django 3.1 on 2020-08-31 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fueltype', '0003_auto_20200831_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='fueltype',
            name='meta',
            field=models.JSONField(null=True),
        ),
    ]