# Generated by Django 5.1.6 on 2025-03-03 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_slider_description_remove_slider_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='name',
            field=models.CharField(default='Slider', max_length=200),
            preserve_default=False,
        ),
    ]
