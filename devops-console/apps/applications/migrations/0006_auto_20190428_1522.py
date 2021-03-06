# Generated by Django 2.1.5 on 2019-04-28 07:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('projects', '0002_auto_20190428_1522'),
        ('applications', '0005_appspec_dependency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'verbose_name': '项目应用'},
        ),
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name': '代码仓库'},
        ),
        migrations.RemoveField(
            model_name='application',
            name='team',
        ),
        migrations.AddField(
            model_name='application',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_applications',
                                    to='projects.Project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='description',
            field=models.TextField(verbose_name='应用描述'),
        ),
        migrations.AlterField(
            model_name='application',
            name='name',
            field=models.CharField(max_length=128, verbose_name='应用名称'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2')], max_length=2, null=True,
                                   verbose_name='应用状态'),
        ),
        migrations.AlterField(
            model_name='application',
            name='type',
            field=models.CharField(choices=[('mircoservice', ''), ('web', ''), ('batch', ''), ('j2se', '')],
                                   max_length=16, verbose_name='应用类型'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='http_url',
            field=models.CharField(max_length=128, null=True, verbose_name='SCM http_url'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='ssh_url',
            field=models.CharField(max_length=128, null=True, verbose_name='SCM ssh_url'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='web_url',
            field=models.CharField(max_length=128, null=True, verbose_name='SCM主页'),
        ),
        migrations.AlterModelTable(
            name='application',
            table='appliations',
        ),
        migrations.AlterModelTable(
            name='repository',
            table='repository',
        ),
    ]
