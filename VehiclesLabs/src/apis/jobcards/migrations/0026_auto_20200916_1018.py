# Generated by Django 3.1 on 2020-09-16 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobcards', '0025_auto_20200915_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcardparts',
            name='partQty',
            field=models.IntegerField(blank=True, max_length=15, null=True),
        ),
    ]
