# Generated by Django 2.1.5 on 2019-10-17 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20190606_1403'),
        ('test', '0005_testgroup_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_test', to='projects.Project', verbose_name='归属项目'),
        ),
        migrations.AddField(
            model_name='testautoplan',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_testAutoPlan', to='projects.Project', verbose_name='归属项目'),
        ),
        migrations.AddField(
            model_name='testenv',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_testEnv', to='projects.Project', verbose_name='归属项目'),
        ),
        migrations.AddField(
            model_name='testgroup',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_testGroup', to='projects.Project', verbose_name='归属项目'),
        ),
        migrations.AddField(
            model_name='testplan',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_testPlan', to='projects.Project', verbose_name='归属项目'),
        ),
    ]
