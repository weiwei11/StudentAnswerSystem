# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-26 10:29
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StudentAnswerApp', '0014_auto_20180324_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='favorite_user',
            field=models.ManyToManyField(related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name=b'Favorite User'),
        ),
        migrations.AlterField(
            model_name='question',
            name='content_description',
            field=ckeditor.fields.RichTextField(verbose_name='Content Description'),
        ),
    ]