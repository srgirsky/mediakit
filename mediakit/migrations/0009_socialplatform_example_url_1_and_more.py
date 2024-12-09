# Generated by Django 5.1.4 on 2024-12-08 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediakit', '0008_remove_socialplatform_age_13_17_percentage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialplatform',
            name='example_url_1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='socialplatform',
            name='example_url_2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='socialplatform',
            name='example_url_3',
            field=models.URLField(blank=True, null=True),
        ),
    ]