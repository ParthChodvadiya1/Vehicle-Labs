# Generated by Django 3.1 on 2020-10-06 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0011_auto_20201006_0954'),
        ('workshop', '0005_auto_20200910_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopdetail',
            name='logo',
        ),
        migrations.AddField(
            model_name='workshopdetail',
            name='media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='media.mediadetails'),
        ),
    ]
