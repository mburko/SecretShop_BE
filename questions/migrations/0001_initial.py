# Generated by Django 4.0.3 on 2022-04-16 22:33

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=40, unique=True, validators=[django.core.validators.RegexValidator(regex='^#[a-zA-Z0-9#\\+\\-]{1,40}')])),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(20)])),
                ('text_body', models.CharField(max_length=1500, validators=[django.core.validators.MinLengthValidator(20)])),
                ('status', models.CharField(blank=True, choices=[(1, 'Opened'), (0, 'Closed')], default=1, max_length=2)),
                ('date_of_publication', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('number_of_views', models.IntegerField(blank=True, default=0)),
                ('number_of_comments', models.IntegerField(blank=True, default=0)),
                ('number_of_likes', models.IntegerField(blank=True, default=0)),
                ('number_of_dislikes', models.IntegerField(blank=True, default=0)),
                ('fame_index', models.FloatField(blank=True, default=1)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='questions.tags')),
            ],
        ),
    ]
