# Generated by Django 2.1.5 on 2019-04-18 03:18

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('teams', '0005_auto_20190418_0746'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='member',
            table='members',
        ),
        migrations.AlterModelTable(
            name='team',
            table='teams',
        ),
    ]
