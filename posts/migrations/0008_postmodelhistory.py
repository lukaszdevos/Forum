# Generated by Django 3.0 on 2020-01-22 20:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20200112_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModelHistory',
            fields=[
                ('postmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.PostModel')),
                ('history_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            bases=('posts.postmodel',),
        ),
    ]
