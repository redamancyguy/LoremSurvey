# Generated by Django 3.2.2 on 2021-05-24 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CAPTCHA',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(default=None, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default=None, max_length=20, unique=True)),
                ('password', models.CharField(default=None, max_length=100)),
                ('token', models.TextField(default=None, max_length=1024)),
                ('phone', models.CharField(default=None, max_length=15)),
                ('email', models.CharField(default=None, max_length=20)),
                ('emailcode', models.CharField(default=None, max_length=32)),
            ],
        ),
    ]
