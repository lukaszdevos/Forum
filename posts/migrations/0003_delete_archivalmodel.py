# Generated by Django 3.0 on 2020-01-11 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_archivalmodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArchivalModel',
        ),
    ]
