# Generated by Django 3.1 on 2020-12-21 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0019_remove_customerdetail_signature'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='customerdetail',
            index=models.Index(fields=['cusname', 'cusemail', 'cusphone', '-createdAt'], name='customer_cu_cusname_77571f_idx'),
        ),
    ]
