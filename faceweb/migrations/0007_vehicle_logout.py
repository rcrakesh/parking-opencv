# Generated by Django 4.1.13 on 2024-07-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceweb', '0006_delete_allowedperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='vehicle_logout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.BinaryField()),
                ('timestamp', models.DateTimeField()),
                ('format', models.CharField(max_length=10)),
                ('text', models.TextField()),
            ],
        ),
    ]
