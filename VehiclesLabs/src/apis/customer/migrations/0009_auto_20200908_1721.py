# Generated by Django 3.1 on 2020-09-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_auto_20200907_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetail',
            name='cusphone',
            field=models.CharField(max_length=10),
        ),
    ]
