# Generated by Django 5.1.6 on 2025-03-03 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_slider_slider_image_slider_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slider',
            name='description',
        ),
        migrations.RemoveField(
            model_name='slider',
            name='title',
        ),
    ]
