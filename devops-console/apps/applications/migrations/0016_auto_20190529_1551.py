# Generated by Django 2.1.5 on 2019-05-29 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0015_auto_20190516_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='application',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True,
                                       related_name='repo', serialize=False, to='applications.Application'),
        ),
    ]