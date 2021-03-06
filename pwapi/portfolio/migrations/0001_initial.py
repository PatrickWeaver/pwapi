# Generated by Django 2.0.2 on 2018-06-29 19:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('cover', models.BooleanField(default=False)),
                ('caption', models.CharField(max_length=1024)),
                ('url', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=1024)),
                ('slug', models.CharField(max_length=1024, unique=True)),
                ('description', models.TextField(default='')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('project_url', models.CharField(max_length=1024)),
                ('source_url', models.CharField(max_length=1024)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('images', models.ManyToManyField(to='portfolio.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('color', models.CharField(max_length=6)),
                ('slug', models.CharField(max_length=50, unique=True)),
                ('status', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_status', to='portfolio.Tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(related_name='project_tags', to='portfolio.Tag'),
        ),
    ]
