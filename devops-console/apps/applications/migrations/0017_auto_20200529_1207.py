# Generated by Django 2.2.10 on 2020-05-29 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0016_auto_20190529_1551'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppEnv',
        ),
        migrations.DeleteModel(
            name='ApplicationEnvironment',
        ),
        migrations.DeleteModel(
            name='ApplicationSetting',
        ),
    ]
