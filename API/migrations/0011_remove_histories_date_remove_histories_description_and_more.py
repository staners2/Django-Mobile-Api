# Generated by Django 4.0 on 2022-01-01 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0010_rename_ru_title_types_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='histories',
            name='date',
        ),
        migrations.RemoveField(
            model_name='histories',
            name='description',
        ),
        migrations.RemoveField(
            model_name='histories',
            name='number',
        ),
        migrations.RemoveField(
            model_name='histories',
            name='type',
        ),
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(null=True)),
                ('date', models.DateTimeField()),
                ('description', models.TextField(null=True)),
                ('type', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='API.types')),
            ],
        ),
        migrations.AddField(
            model_name='histories',
            name='fact',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='API.fact'),
        ),
    ]
