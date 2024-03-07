# Generated by Django 5.0.2 on 2024-03-02 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyStay', '0016_hotel_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='country',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='facility',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='phone',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
