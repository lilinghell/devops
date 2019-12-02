# Generated by Django 2.1.5 on 2019-05-17 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_remove_project_logo'),
        ('features', '0012_auto_20190517_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='module_features', to='projects.Module', verbose_name='模块'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro_features', to='projects.Project', verbose_name='关联项目'),
        ),
    ]
