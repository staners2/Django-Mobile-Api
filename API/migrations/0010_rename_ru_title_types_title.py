# Generated by Django 4.0 on 2021-12-18 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_histories_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='types',
            old_name='ru_title',
            new_name='title',
        ),
    ]
