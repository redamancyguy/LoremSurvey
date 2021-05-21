# Generated by Django 3.2.2 on 2021-05-19 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0025_auto_20210519_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='desc',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='page',
            name='etime',
            field=models.DateTimeField(blank=True, verbose_name='startTime'),
        ),
        migrations.AlterField(
            model_name='page',
            name='stime',
            field=models.DateTimeField(blank=True, verbose_name='startTime'),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]