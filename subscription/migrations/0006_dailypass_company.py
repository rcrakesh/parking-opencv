# Generated by Django 4.1.13 on 2024-07-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_dailypass'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailypass',
            name='company',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
