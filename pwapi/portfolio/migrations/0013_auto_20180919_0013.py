# Generated by Django 2.1 on 2018-09-19 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0012_auto_20180918_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
