# Generated by Django 5.0.2 on 2024-02-22 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyStay', '0002_booking_name_booking_phone_alter_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='name',
            new_name='reserved_name',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='phone',
            new_name='reserved_phone',
        ),
        migrations.RemoveField(
            model_name='hotelmanager',
            name='position',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='hotelmanager',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='type',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
