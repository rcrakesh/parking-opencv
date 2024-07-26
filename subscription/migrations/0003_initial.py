# Generated by Django 4.1.13 on 2024-07-19 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscription', '0002_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('subscription_id', models.IntegerField()),
            ],
        ),
    ]