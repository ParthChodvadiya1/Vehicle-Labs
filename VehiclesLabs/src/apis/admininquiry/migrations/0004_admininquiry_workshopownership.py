# Generated by Django 3.1 on 2020-11-23 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admininquiry', '0003_admininquiry_usertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='admininquiry',
            name='workshopOwnership',
            field=models.CharField(blank=True, max_length=450, null=True),
        ),
    ]
