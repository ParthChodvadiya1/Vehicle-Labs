# Generated by Django 3.1 on 2020-10-08 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0009_auto_20201007_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopdetail',
            name='expected_days',
        ),
        migrations.AddField(
            model_name='workshopdetail',
            name='expectedDay',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
