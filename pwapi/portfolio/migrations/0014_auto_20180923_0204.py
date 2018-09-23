# Generated by Django 2.1 on 2018-09-23 02:04

from django.db import migrations, models
import portfolio.models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0013_auto_20180919_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='upload',
            field=models.FileField(default=False, upload_to=portfolio.models.upload_file),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='uuid',
            field=models.CharField(blank=True, max_length=1024, unique=True),
        ),
    ]
