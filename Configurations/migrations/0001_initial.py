# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-11 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_theme', models.CharField(choices=[(b'Datasystems', b'Datasystems'), (b'Cameroun', b'Cameroun')], default=None, max_length=20, verbose_name=b'S\xc3\xa9lectionner le th\xc3\xa8me')),
            ],
        ),
    ]
