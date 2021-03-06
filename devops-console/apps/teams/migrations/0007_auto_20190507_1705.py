# Generated by Django 2.1.5 on 2019-05-07 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20190418_1118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['-created_at', 'access_level']},
        ),
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='描述信息'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=128, null=True, unique=True, verbose_name='TeamName'),
        ),
    ]
