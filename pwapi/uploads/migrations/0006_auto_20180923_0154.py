# Generated by Django 2.1 on 2018-09-23 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0005_auto_20180923_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='uuid',
            field=models.CharField(blank=True, default='', max_length=1024, unique=True),
        ),
    ]
