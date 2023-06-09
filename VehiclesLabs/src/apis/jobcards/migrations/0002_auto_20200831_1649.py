# Generated by Django 3.1 on 2020-08-31 11:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobcards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcarddetail',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobcarddetail',
            name='createdBy',
            field=models.CharField(default=django.utils.timezone.now, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobcarddetail',
            name='isDeleted',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='jobcarddetail',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='jobcarddetail',
            name='updatedBy',
            field=models.CharField(default=django.utils.timezone.now, max_length=120),
            preserve_default=False,
        ),
    ]
