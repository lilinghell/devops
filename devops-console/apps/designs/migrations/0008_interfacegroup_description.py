# Generated by Django 2.1.5 on 2019-09-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0007_interfaces_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='interfacegroup',
            name='description',
            field=models.TextField(null=True, verbose_name='描述'),
        ),
    ]
