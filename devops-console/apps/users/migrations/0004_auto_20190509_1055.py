# Generated by Django 2.1.5 on 2019-05-09 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_merge_20190508_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=128, null=True, verbose_name='Name'),
        ),
    ]
