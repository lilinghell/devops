# Generated by Django 2.1.5 on 2019-02-01 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0003_auto_20190130_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='project_id',
            field=models.IntegerField(null=True),
        ),
    ]