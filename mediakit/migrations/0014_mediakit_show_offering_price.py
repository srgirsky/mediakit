# Generated by Django 5.1.4 on 2024-12-13 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediakit', '0013_mediakit_url_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediakit',
            name='show_offering_price',
            field=models.BooleanField(default=True),
        ),
    ]