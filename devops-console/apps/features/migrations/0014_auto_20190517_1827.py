# Generated by Django 2.1.5 on 2019-05-17 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0013_auto_20190517_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feature',
            old_name='applications',
            new_name='apps',
        ),
    ]
