# Generated by Django 2.1.4 on 2019-01-06 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timelinecontent',
            old_name='content',
            new_name='contents',
        ),
    ]
