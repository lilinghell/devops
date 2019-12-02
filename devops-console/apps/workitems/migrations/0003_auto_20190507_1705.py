# Generated by Django 2.1.5 on 2019-05-07 09:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workitems', '0002_auto_20190506_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workitem',
            name='assignee_users',
            field=models.ManyToManyField(blank=True, related_name='user_workitems', to=settings.AUTH_USER_MODEL, verbose_name='分配开发人员'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='status',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], default='0', max_length=2),
        ),
    ]