# Generated by Django 2.1.5 on 2019-09-20 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20190606_1403'),
        ('designs', '0005_auto_20190920_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='interfacegroup',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_group', to='projects.Project', verbose_name='归属项目'),
        ),
    ]
