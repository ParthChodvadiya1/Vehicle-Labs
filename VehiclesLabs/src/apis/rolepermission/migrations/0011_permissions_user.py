# Generated by Django 3.1 on 2020-09-25 13:14

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rolepermission', '0010_remove_permissions_countersale'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissions',
            name='user',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Create', 'Create'), ('Delete', 'Delete'), ('Update', 'Update'), ('View', 'View')], max_length=25, null=True),
        ),
    ]
