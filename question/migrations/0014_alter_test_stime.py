# Generated by Django 3.2.2 on 2021-05-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0013_auto_20210515_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='stime',
            field=models.DateTimeField(auto_now=True, verbose_name='startTime'),
        ),
    ]
