# Generated by Django 3.1 on 2020-09-09 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20200908_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediadetails',
            name='mediaFor',
            field=models.CharField(blank=True, choices=[('1', 'USER_PROFILE'), ('2', 'WORKSHOP_PROFILE')], max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='mediadetails',
            name='mediaType',
            field=models.CharField(blank=True, choices=[('1', 'Image'), ('2', 'Video')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mediadetails',
            name='mediaURL',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]