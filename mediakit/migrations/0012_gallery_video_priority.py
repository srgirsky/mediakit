# Generated by Django 5.1.4 on 2024-12-13 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediakit', '0011_gallery_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='video_priority',
            field=models.IntegerField(default=1),
        ),
    ]