# Generated by Django 2.0.2 on 2018-10-03 01:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1024, null=True)),
                ('slug', models.CharField(blank=True, max_length=1024, unique=True)),
                ('body', models.TextField()),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('is_hidden', models.BooleanField(default=False)),
            ],
        ),
    ]
