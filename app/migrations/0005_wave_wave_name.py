# Generated by Django 2.1.15 on 2021-01-10 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210110_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='wave',
            name='wave_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
