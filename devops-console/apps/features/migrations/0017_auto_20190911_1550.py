# Generated by Django 2.1.5 on 2019-09-11 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0016_auto_20190605_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='apps',
            field=models.ManyToManyField(related_name='app_features', to='applications.Application', verbose_name='关联应用'),
        ),
    ]
