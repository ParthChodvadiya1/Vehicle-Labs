# Generated by Django 3.1 on 2020-12-21 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_software', '0003_auto_20201204_1142'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='accounting',
            index=models.Index(fields=['refType', 'refID', '-createdAt'], name='accounting__refType_f5972d_idx'),
        ),
    ]
