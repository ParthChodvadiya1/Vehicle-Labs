# Generated by Django 3.1 on 2020-12-21 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0014_auto_20201012_1301'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='mediadetails',
            index=models.Index(fields=['mediaType', '-createdAt'], name='media_media_mediaTy_6d2d10_idx'),
        ),
    ]
