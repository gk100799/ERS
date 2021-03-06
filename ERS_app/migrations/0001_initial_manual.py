# Generated by Django 2.2.5 on 2019-11-03 15:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ERSEvent',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('description', models.TextField(blank=True)),
                ('organizers', models.CharField(blank=True, max_length=15)),
                ('venue', models.CharField(blank=True, max_length=20)),
                ('time', models.TimeField()),
                ('date', models.DateField(blank=True)),
                ('limit', models.IntegerField(blank=True)),
                ('fee', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ERSQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=75)),
                ('option1', models.CharField(blank=True, max_length=30, null=True)),
                ('option2', models.CharField(blank=True, max_length=30, null=True)),
                ('option3', models.CharField(blank=True, max_length=30, null=True)),
                ('option4', models.CharField(blank=True, max_length=30, null=True)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERS.ERSEvent')),
            ],
        ),
        migrations.CreateModel(
            name='ERSSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField(max_length=50)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERS.ERSEvent')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERS.ERSQuestion')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
