# Generated by Django 2.1.5 on 2019-05-09 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190509_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=128, null=True, verbose_name='Name'),
        ),
    ]
