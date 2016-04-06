# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-06 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('createSurvey', '0011_auto_20160406_1229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ruolofuturo',
            old_name='livello_cariera',
            new_name='persona',
        ),
        migrations.RenameField(
            model_name='ruolopregresso',
            old_name='livello_cariera',
            new_name='persona',
        ),
        migrations.RemoveField(
            model_name='ruoloattuale',
            name='livello_cariera',
        ),
        migrations.AddField(
            model_name='ruoloattuale',
            name='ruolo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='createSurvey.Ruolo'),
        ),
        migrations.AddField(
            model_name='ruolofuturo',
            name='ruolo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='createSurvey.Ruolo'),
        ),
        migrations.AddField(
            model_name='ruolopregresso',
            name='ruolo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='createSurvey.Ruolo'),
        ),
    ]
