# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-19 14:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudentAnswerApp', '0012_auto_20180312_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_members',
            field=models.ManyToManyField(null=True, related_name='joined_classes', to=settings.AUTH_USER_MODEL, verbose_name='Class Member'),
        ),
        migrations.AlterField(
            model_name='question',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_questions', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='subanswer',
            name='belong_to_answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_answers', to='StudentAnswerApp.Answer', verbose_name='Belong To Answer'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='belong_to_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_questions', to='StudentAnswerApp.Question', verbose_name='Belong To Queston'),
        ),
    ]
