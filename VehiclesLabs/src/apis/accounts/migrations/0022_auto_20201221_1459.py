# Generated by Django 3.1 on 2020-12-21 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20201110_1221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdetail',
            options={},
        ),
        migrations.AddIndex(
            model_name='userdetail',
            index=models.Index(fields=['utype', 'username', 'email', 'userphone', 'expiredAt', 'isActivated', '-createdAt'], name='accounts_us_utype_9c1498_idx'),
        ),
    ]
