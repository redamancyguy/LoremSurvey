# Generated by Django 3.2.2 on 2021-05-13 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.TextField(default=None, max_length=1024),
        ),
    ]