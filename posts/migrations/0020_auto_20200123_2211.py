# Generated by Django 3.0 on 2020-01-23 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20200123_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodelhistory',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_history', to='posts.PostModel'),
        ),
    ]