# Generated by Django 3.0 on 2020-01-23 19:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20200122_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModelHistory',
            fields=[
                ('text_area_edited', models.TextField()),
                ('history_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.PostModel')),
            ],
            bases=('posts.postmodel',),
        ),
    ]