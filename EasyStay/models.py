from django.db import models
from django.utils import timezone


# Create your models here.

class user(models.Model):
    user_id = models.CharField(max_length=10, default=None)
    username = models.CharField(max_length=50, default=None)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, default='+0000000000')
    password = models.CharField(max_length=50)


class hotelmanager(models.Model):
    hotel_name = models.CharField(max_length=50, default=None)
    manage_id = models.CharField(max_length=10, default=None)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, default='+0000000000')
    password = models.CharField(max_length=50)


class hotel(models.Model):
    manager = models.ForeignKey(hotelmanager, on_delete=models.CASCADE)
    hotel_id = models.CharField(max_length=10, default=None)
    name = models.CharField(max_length=100, default=None)
    city = models.CharField(max_length=50, default='London', blank=True)
    country = models.CharField(max_length=50, default='Great Britain', blank=True)
    location = models.CharField(max_length=255, default='default_location')
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, default='+0000000000')
    star = models.IntegerField(default=3)
    description = models.TextField(default='No description provided.')
    facility = models.TextField(default='Basic facilities.')
    image = models.ImageField(upload_to='hotel_image', default=None)


class roomtype(models.Model):
    
    id = models.CharField(max_length=10, primary_key=True)
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)
    facility = models.TextField(default='Basic room facilities.')
    image = models.ImageField(upload_to='room_image',default=None)
    guests = models.IntegerField(default=2)


class room(models.Model):
    type = models.ForeignKey(roomtype, on_delete=models.CASCADE)
    Room_number = models.CharField(max_length=10, default='001')
    availability = models.BooleanField(default=True)  # True for available, False for unavailable

class booking(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    room_number = models.ForeignKey(room, on_delete=models.CASCADE)
    ref_num = models.CharField(max_length=50, default='REF0001')
    booking_date = models.DateTimeField(default=timezone.now)

    from_date = models.DateField(default=None)####
    to_date = models.DateField(default=None)####

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    reserved_name = models.CharField(max_length=50, default='Name')
    reserved_phone = models.CharField(max_length=50, default='Phone')
    status = models.IntegerField(default='1')  # '1' for wait check-in//'2'checked in //'3'checked out

    check_in_date = models.DateTimeField(null=True, blank=True)####
    check_out_date = models.DateTimeField(null=True, blank=True)####

    review_star = models.IntegerField(null=True, blank=True)
    review_comment = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
