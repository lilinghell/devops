# Generated by Django 2.1.5 on 2019-09-29 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0004_auto_20190929_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='testgroup',
            name='description',
            field=models.TextField(null=True, verbose_name='描述'),
        ),
    ]
