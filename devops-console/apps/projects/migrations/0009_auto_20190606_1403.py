# Generated by Django 2.1.5 on 2019-06-06 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at']},
        ),
    ]
