# Generated by Django 2.1.5 on 2019-02-01 04:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0002_auto_20190126_1056'),
        ('teams', '0003_auto_20190130_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128, verbose_name='TeamName')),
                ('description', models.TextField(null=True)),
                ('color', models.CharField(max_length=16)),
                ('type', models.CharField(
                    choices=[('userlabel', 'userlabel'), ('applabel', 'applabel'), ('tasklabel', 'tasklabel'),
                             ('featurelabel', 'featurelabel'), ('reqlabel', 'reqlabel')], max_length=16, null=True)),
                ('created_by', models.ForeignKey(on_delete=models.SET(-999), to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'labels',
            },
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together={('title', 'team', 'org')},
        ),
    ]