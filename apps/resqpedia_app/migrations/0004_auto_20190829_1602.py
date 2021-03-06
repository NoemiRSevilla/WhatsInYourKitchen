# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-29 16:02
from __future__ import unicode_literals

import apps.resqpedia_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resqpedia_app', '0003_auto_20190829_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=100, validators=[apps.resqpedia_app.models.LengthGreaterThanOne, apps.resqpedia_app.models.NameMatchforRegex, apps.resqpedia_app.models.LengthGreaterThanTwo]),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, validators=[apps.resqpedia_app.models.LengthGreaterThanOne, apps.resqpedia_app.models.NameMatchforRegex, apps.resqpedia_app.models.LengthGreaterThanTwo]),
        ),
    ]
