# Generated by Django 5.1 on 2024-09-25 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_room_room_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='name',
            new_name='account',
        ),
    ]
