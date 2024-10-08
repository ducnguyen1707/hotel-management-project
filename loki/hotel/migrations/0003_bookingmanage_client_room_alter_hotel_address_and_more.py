# Generated by Django 5.0.7 on 2024-09-12 07:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingManage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_time', models.DateTimeField()),
                ('check_out_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('id_number', models.CharField(max_length=12, unique=True)),
                ('vehicle', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.IntegerField()),
                ('room_type', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('floor', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='phone_number',
            field=models.CharField(max_length=11),
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.IntegerField(default=0)),
                ('tax', models.FloatField(default=0.1)),
                ('booking_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hotel.bookingmanage')),
            ],
        ),
        migrations.AddField(
            model_name='bookingmanage',
            name='client',
            field=models.ManyToManyField(related_name='booking_client', to='hotel.client'),
        ),
        migrations.AddField(
            model_name='bookingmanage',
            name='room',
            field=models.ManyToManyField(related_name='booking_room', to='hotel.room'),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=50)),
                ('status', models.BooleanField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_name', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('staff', models.ManyToManyField(to='hotel.staff')),
            ],
        ),
    ]
