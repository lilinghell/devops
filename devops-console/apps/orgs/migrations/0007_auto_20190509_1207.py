# Generated by Django 2.1.5 on 2019-05-09 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0006_auto_20190429_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='comment',
        ),
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, default='', max_length=128, verbose_name='description'),
        ),
    ]
