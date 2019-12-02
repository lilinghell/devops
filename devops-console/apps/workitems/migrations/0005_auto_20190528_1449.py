# Generated by Django 2.1.5 on 2019-05-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('workitems', '0004_merge_20190508_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workitem',
            name='end_date',
            field=models.CharField(max_length=8, null=True, verbose_name='结束日期YYYYMMDD'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='estimate_time',
            field=models.IntegerField(null=True, verbose_name='时间预估'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='important',
            field=models.IntegerField(default=2, verbose_name='重要性'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='priority',
            field=models.IntegerField(default=2, verbose_name='优先级'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='start_date',
            field=models.CharField(max_length=8, null=True, verbose_name='开始日期YYYYMMDD'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='status',
            field=models.CharField(
                choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                default='1', max_length=2),
        ),
    ]