# Generated by Django 3.1 on 2020-09-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_workshopdetail_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopdetail',
            name='isDeleted',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
