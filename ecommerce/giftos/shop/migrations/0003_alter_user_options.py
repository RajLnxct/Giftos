# Generated by Django 5.1.6 on 2025-02-28 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_user_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': 'Register'},
        ),
    ]
