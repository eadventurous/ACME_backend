# Generated by Django 2.1.2 on 2018-11-11 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_auto_20181111_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveryoperator',
            old_name='current_location',
            new_name='location',
        ),
    ]
