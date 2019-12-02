# Generated by Django 2.1.5 on 2019-04-28 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('applications', '0006_auto_20190428_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='project_applications', to='projects.Project'),
        ),
        migrations.AlterModelTable(
            name='repository',
            table='repositorys',
        ),
    ]