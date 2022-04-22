# Generated by Django 4.0.3 on 2022-04-16 22:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9\\_\\-\\.]*$'), django.core.validators.MinLengthValidator(5)])),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('avatar', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(regex='^([a-zA-Z0-9\\_\\-\\.]+\\\\[a-zA-Z0-9\\_\\-\\.]+)+$')])),
                ('role', models.CharField(blank=True, choices=[(1, 'User'), (2, 'Admin'), (3, 'Premium')], default=1, max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
