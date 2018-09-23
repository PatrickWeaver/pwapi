# Generated by Django 2.1 on 2018-09-23 02:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0014_auto_20180923_0204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='upload',
        ),
        migrations.AlterField(
            model_name='image',
            name='uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, unique=True),
        ),
    ]