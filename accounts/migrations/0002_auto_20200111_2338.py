# Generated by Django 3.0 on 2020-01-11 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='default.jpg', upload_to='profile'),
        ),
    ]
