# Generated by Django 3.1 on 2020-10-28 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admininquiry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admininquiry',
            name='garageName',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]