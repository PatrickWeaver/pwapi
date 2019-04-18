# Generated by Django 2.1.5 on 2019-01-31 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blob',
            name='redirect',
            field=models.TextField(default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='blob',
            name='is_hidden',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]