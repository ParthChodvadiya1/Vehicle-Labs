# Generated by Django 3.1 on 2020-10-07 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobcards', '0030_auto_20201007_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCardImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, upload_to='')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobcards.jobcarddetail')),
            ],
        ),
    ]
