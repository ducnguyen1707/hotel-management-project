# Generated by Django 5.1 on 2024-10-04 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0009_alter_staff_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price',
            field=models.CharField(choices=[('200000', '200,000 VND'), ('300000', '300,000 VND')], max_length=50),
        ),
    ]
