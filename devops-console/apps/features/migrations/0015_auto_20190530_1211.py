# Generated by Django 2.1.5 on 2019-05-30 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0016_auto_20190529_1551'),
        ('features', '0014_auto_20190517_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurebranch',
            name='app',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='app_branch', to='applications.Application'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='featurebranch',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='featurebranch',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_branch', to='features.Feature', verbose_name='分支关联需求'),
        ),
        migrations.RemoveField(
            model_name='featurebranch',
            name='repository',
        ),
        migrations.AlterUniqueTogether(
            name='featurebranch',
            unique_together={('feature', 'app')},
        ),
    ]