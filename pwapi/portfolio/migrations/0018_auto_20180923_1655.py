# Generated by Django 2.1 on 2018-09-23 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0017_auto_20180923_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='order',
            field=models.IntegerField(blank=True, unique=True),
        ),
    ]
