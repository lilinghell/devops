# Generated by Django 2.1.5 on 2019-04-30 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0004_auto_20190430_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_features', to='projects.Project', verbose_name='关联项目'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='status',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=2, verbose_name='需求状态'),
        ),
    ]