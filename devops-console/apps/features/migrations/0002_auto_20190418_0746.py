# Generated by Django 2.1.5 on 2019-04-17 23:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requirements', '0001_initial'),
        ('orgs', '0005_auto_20190418_0728'),
        ('applications', '0005_appspec_dependency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('features', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='requirement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='req_features', to='requirements.Requirement', verbose_name='上级需求'),
        ),
        migrations.AddField(
            model_name='featurebranch',
            name='created_by',
            field=models.ForeignKey(on_delete=models.SET(-999), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='featurebranch',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization'),
        ),
        migrations.AddField(
            model_name='featurebranch',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repo_branchs', to='applications.Repository'),
        ),
    ]