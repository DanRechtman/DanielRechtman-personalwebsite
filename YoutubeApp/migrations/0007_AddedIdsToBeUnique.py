# Generated by Django 4.2.5 on 2023-11-02 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YoutubeApp', '0006_Added_UserWatching'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwatching',
            name='MovieId',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userwatching',
            name='TvShowId',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
