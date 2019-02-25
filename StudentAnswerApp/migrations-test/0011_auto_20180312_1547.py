# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentAnswerApp', '0010_auto_20180311_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='class_questions',
        ),
        migrations.RemoveField(
            model_name='subquestion',
            name='correction_rate',
        ),
        migrations.AddField(
            model_name='question',
            name='share_classes',
            field=models.ManyToManyField(default=b'null', null=True, to='StudentAnswerApp.Class', verbose_name='Share To Classes'),
        ),
        migrations.AddField(
            model_name='subanswer',
            name='correction_rate',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Correction Rate'),
        ),
        migrations.AddField(
            model_name='subquestion',
            name='kind',
            field=models.CharField(choices=[(b'choice', 'choice'), (b'gap filling', 'gap filling'), (b'short answer', 'short answer'), (b'other', 'other')], default=b'other', max_length=20, verbose_name='Kind'),
        ),
    ]
