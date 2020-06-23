# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2020-06-23 09:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campuses',
            options={'verbose_name': '校区', 'verbose_name_plural': '校区'},
        ),
        migrations.AlterModelOptions(
            name='classlist',
            options={'verbose_name': '已报班级', 'verbose_name_plural': '已报班级'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '客户', 'verbose_name_plural': '客户'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator("[\\w!#$%&'*+/=?^_`{|}~-]+(?:\\.[\\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\\w](?:[\\w-]*[\\w])?\\.)+[\\w](?:[\\w-]*[\\w])?")]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, default=None, max_length=32, null=True, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$')], verbose_name='手机'),
        ),
    ]
