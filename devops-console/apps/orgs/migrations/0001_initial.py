# Generated by Django 2.1.5 on 2019-01-26 02:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('created_by', models.IntegerField(blank=True, null=True, verbose_name='Created By')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='Comment')),
            ],
            options={
                'verbose_name': 'Organization',
            },
        ),
    ]
