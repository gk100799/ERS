# Generated by Django 2.2.5 on 2019-11-03 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERS', '0004_auto_20191103_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ersevent',
            name='event_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
