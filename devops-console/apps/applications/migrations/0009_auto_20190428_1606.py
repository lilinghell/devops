# Generated by Django 2.1.5 on 2019-04-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0008_auto_20190428_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='scm_url',
            field=models.CharField(max_length=128, verbose_name='SCM_url'),
        ),
    ]