# Generated by Django 3.1 on 2020-09-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0002_auto_20200908_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partdetails',
            name='isDeleted',
            field=models.BooleanField(null=True),
        ),
    ]
