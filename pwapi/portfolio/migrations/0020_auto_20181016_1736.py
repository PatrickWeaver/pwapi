# Generated by Django 2.1.2 on 2018-10-16 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0019_project_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='alt_text',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='caption',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
