# Generated by Django 2.2.5 on 2019-11-03 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERS', '0002_auto_20191103_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ersevent',
            old_name='name',
            new_name='event_name',
        ),
    ]
