# Generated by Django 3.1 on 2020-09-08 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_delete_jobcardservices'),
        ('jobcards', '0003_jobcarddetail_meta'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobcardServices',
            fields=[
                ('jobcardServidesID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('meta', models.JSONField(null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(null=True)),
                ('createdBy', models.CharField(max_length=120)),
                ('updatedBy', models.CharField(max_length=120)),
                ('jobID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobcards.jobcarddetail')),
                ('serviceID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.servicedetails')),
            ],
        ),
    ]