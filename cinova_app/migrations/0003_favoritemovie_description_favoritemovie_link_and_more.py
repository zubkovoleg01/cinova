# Generated by Django 4.2.5 on 2023-10-09 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinova_app', '0002_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritemovie',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='favoritemovie',
            name='link',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='favoritemovie',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='favoritemovie',
            name='poster',
            field=models.ImageField(null=True, upload_to='cinova_app/images'),
        ),
        migrations.AddField(
            model_name='favoritemovie',
            name='rating',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='favoritemovie',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
