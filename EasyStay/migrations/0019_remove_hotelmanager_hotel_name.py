# Generated by Django 5.0.2 on 2024-03-03 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EasyStay', '0018_alter_booking_ref_num_alter_booking_reserved_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelmanager',
            name='hotel_name',
        ),
    ]
