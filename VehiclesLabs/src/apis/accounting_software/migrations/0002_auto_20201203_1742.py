# Generated by Django 3.1 on 2020-12-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_software', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounting',
            name='createdBy',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='updatedBy',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]