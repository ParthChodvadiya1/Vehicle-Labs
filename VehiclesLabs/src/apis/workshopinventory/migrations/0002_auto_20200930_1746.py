# Generated by Django 3.1 on 2020-09-30 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshopinventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshopinventory',
            old_name='min_qty',
            new_name='minimum_qty',
        ),
    ]
