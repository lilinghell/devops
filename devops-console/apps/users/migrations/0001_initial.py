# Generated by Django 2.1.5 on 2019-01-26 02:56

import common.utils
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=128, unique=True, verbose_name='Username')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='Email')),
                ('avatar', models.ImageField(null=True, upload_to='avatar', verbose_name='Avatar')),
                ('wechat', models.CharField(blank=True, max_length=128, verbose_name='Wechat')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('comment', models.TextField(blank=True, max_length=200, verbose_name='Comment')),
                ('is_first_login', models.BooleanField(default=True)),
                ('date_expired',
                 models.DateTimeField(blank=True, db_index=True, default=common.utils.date_expired_default, null=True,
                                      verbose_name='Date expired')),
                ('created_by', models.CharField(default='', max_length=30, verbose_name='Created by')),
                ('source', models.CharField(choices=[('local', 'Local'), ('ldap', 'LDAP/AD'), ('openid', 'OpenID')],
                                            default='local', max_length=30, verbose_name='Source')),
                ('date_password_last_updated',
                 models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date password last updated')),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group',
                                                  verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='Username')),
                ('type', models.CharField(choices=[('W', 'Web')], max_length=2, verbose_name='Login type')),
                ('ip', models.GenericIPAddressField(verbose_name='Login ip')),
                ('reason', models.SmallIntegerField(
                    choices=[(0, '-'), (1, 'Username/password check failed'), (2, 'MFA authentication failed'),
                             (3, 'Username does not exist'), (4, 'Password expired')], default=0,
                    verbose_name='Reason')),
                ('status',
                 models.BooleanField(choices=[(True, 'Success'), (False, 'Failed')], default=True, max_length=2,
                                     verbose_name='Status')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Date login')),
            ],
            options={
                'ordering': ['-datetime', 'username'],
            },
        )
    ]