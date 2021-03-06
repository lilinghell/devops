# Generated by Django 2.1.5 on 2019-05-06 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('projects', '0003_auto_20190506_1822'),
        ('workitems', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workitem',
            name='application',
        ),
        migrations.RemoveField(
            model_name='workitem',
            name='team',
        ),
        migrations.AddField(
            model_name='workitem',
            name='attachments',
            field=models.ManyToManyField(blank=True, related_name='workitem_attachments', to='common.Attachment', verbose_name='工作项附件'),
        ),
        migrations.AddField(
            model_name='workitem',
            name='description_html',
            field=models.TextField(null=True, verbose_name='描述HTML'),
        ),
        migrations.AddField(
            model_name='workitem',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='label_workitems', to='projects.Label', verbose_name='工作项标签'),
        ),
        migrations.AddField(
            model_name='workitem',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='module_workitems', to='projects.Module', verbose_name='归属模块'),
        ),
        migrations.AddField(
            model_name='workitem',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_workitems', to='projects.Project', verbose_name='关联项目'),
        ),
        migrations.AddField(
            model_name='workitem',
            name='type',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('9', '9')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='assignee_users',
            field=models.ManyToManyField(related_name='user_workitems', to=settings.AUTH_USER_MODEL, verbose_name='分配开发人员'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='end_date',
            field=models.CharField(max_length=8, verbose_name='结束日期YYYYMMDD'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='feature',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feature_workitems', to='features.Feature', verbose_name='关联需求'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_workitems', to='workitems.WorkItem', verbose_name='父工作项'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='start_date',
            field=models.CharField(max_length=8, verbose_name='开始日期YYYYMMDD'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='status',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=2),
        ),
    ]
