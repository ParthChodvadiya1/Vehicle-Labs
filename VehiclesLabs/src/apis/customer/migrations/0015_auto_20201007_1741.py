# Generated by Django 3.1 on 2020-10-07 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_customerdetail_cussignature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetail',
            name='cussignature',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
