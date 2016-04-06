# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-16 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createSurvey', '0002_column_num_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='column',
            name='name',
        ),
        migrations.AddField(
            model_name='column',
            name='description',
            field=models.CharField(default='', max_length=2048),
        ),
        migrations.AddField(
            model_name='column',
            name='jsonCode',
            field=models.CharField(default='', max_length=4096),
        ),
        migrations.AddField(
            model_name='column',
            name='label',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='column',
            name='option',
            field=models.CharField(default='', max_length=2048),
        ),
        migrations.AddField(
            model_name='column',
            name='required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='column',
            name='type',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.DeleteModel(
            name='Domain',
        ),
    ]