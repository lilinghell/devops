# Generated by Django 2.1.5 on 2019-09-20 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20190606_1403'),
        ('designs', '0006_interfacegroup_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='interfaces',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_interface', to='projects.Project', verbose_name='归属项目'),
        ),
    ]
