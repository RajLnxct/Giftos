# Generated by Django 5.1.6 on 2025-02-28 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='number',
        ),
    ]
