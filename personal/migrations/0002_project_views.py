# Generated by Django 2.2 on 2019-07-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
