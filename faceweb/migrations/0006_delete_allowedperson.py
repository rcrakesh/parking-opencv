# Generated by Django 4.1.13 on 2024-07-20 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faceweb', '0005_vehicle_login_delete_mongodbsnapshot'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AllowedPerson',
        ),
    ]
