# Generated by Django 5.1.4 on 2024-12-12 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediakit', '0010_alter_gallery_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='platform',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]