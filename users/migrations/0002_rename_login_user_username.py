# Generated by Django 4.0.3 on 2022-04-09 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='login',
            new_name='username',
        ),
    ]
