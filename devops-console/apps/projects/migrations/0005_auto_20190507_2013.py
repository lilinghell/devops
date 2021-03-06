# Generated by Django 2.1.5 on 2019-05-07 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20190507_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='logo',
            field=models.ImageField(null=True, upload_to='', verbose_name='项目LOGO'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(),
        ),
    ]
