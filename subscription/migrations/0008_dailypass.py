# Generated by Django 4.1.13 on 2024-07-26 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0007_delete_dailypass'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pass_code', models.IntegerField()),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('company', models.CharField(max_length=20)),
                ('num_people', models.IntegerField(default=1)),
                ('reference_name', models.CharField(max_length=100)),
            ],
        ),
    ]
