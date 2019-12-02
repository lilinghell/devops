# Generated by Django 2.1.5 on 2019-01-27 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('orgs', '0002_auto_20190126_1056'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source_id', models.IntegerField(verbose_name='来源ID')),
                ('source_type',
                 models.CharField(choices=[('team', 'team'), ('application', 'application')], default='team',
                                  max_length=32)),
                ('type',
                 models.CharField(choices=[('TeamMember', 'TeamMember'), ('AppMember', 'AppMember')], max_length=32)),
                ('notification_level', models.IntegerField(null=True, verbose_name='notification_level')),
                ('created_by', models.ForeignKey(on_delete=models.SET(-999), to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, verbose_name='TeamName')),
                ('description', models.TextField()),
                ('visit_level', models.IntegerField(choices=[(10, '公开'), (90, '私有')], verbose_name='访问级别')),
                ('created_by', models.ForeignKey(on_delete=models.SET(-999), to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
                ('owner',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_teams',
                                   to=settings.AUTH_USER_MODEL, verbose_name='小组负责人')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             related_name='child_teams', to='teams.Team', verbose_name='上级team')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TeamRole',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True,
                                          verbose_name='TeamName')),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='teamroles',
            field=models.ManyToManyField(related_name='team_members', to='teams.TeamRole'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('source_id', 'user')},
        ),
    ]
