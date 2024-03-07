from django.db import models
from django.utils import timezone


# Create your models here.
'''__  User Table __'''
class user(models.Model):
    user_id = models.CharField(max_length=10, default=None)
    username = models.CharField(max_length=50, default=None)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, default='+0000000000')
    password = models.CharField(max_length=50)

'''__  Manager Table __'''
class hotelmanager(models.Model):
    manage_id = models.CharField(max_length=10, default=None)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, default='+0000000000')
    password = models.CharField(max_length=50)

'''__  Hotel Table __'''
class hotel(models.Model):
    manager = models.ForeignKey(hotelmanager, on_delete=models.CASCADE)
    hotel_id = models.CharField(max_length=10, default=None)
    name = models.CharField(max_length=100, default=None)
    country = models.CharField(max_length=50, default=None)
    city = models.CharField(max_length=50, default=None)
    location = models.CharField(max_length=255, default=None)
    postcode = models.CharField(max_length=50, default=None)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, default=None)
    star = models.IntegerField(default=3)
    description = models.TextField(default=None)
    facility = models.TextField(default=None)
    image = models.ImageField(upload_to='hotel_image', default=None)

'''__  Room Type Table __'''
class roomtype(models.Model):
    
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None)
    guests = models.IntegerField(default=2)
    facility = models.TextField(default=None)
    image = models.ImageField(upload_to='room_image',default=None)
    guests = models.IntegerField(default=2)

'''__  Room Table __'''
class room(models.Model):
    type = models.ForeignKey(roomtype, on_delete=models.CASCADE)
    Room_number = models.CharField(max_length=10, default=None)
    availability = models.BooleanField(default=True)  # True for available, False for unavailable

'''__  Booking Table __'''
class booking(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    room_number = models.ForeignKey(room, on_delete=models.CASCADE)
    ref_num = models.CharField(max_length=50, default=None)
    booking_date = models.DateTimeField(default=timezone.now)

    from_date = models.DateField(default=None)
    to_date = models.DateField(default=None)

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    reserved_name = models.CharField(max_length=50, default=None)
    reserved_phone = models.CharField(max_length=50, default=None)

    status = models.IntegerField(default='1')  # '1' for wait check-in//'2'checked in //'3'checked out // '4' not come

    check_in_date = models.DateTimeField(null=True, blank=True)
    check_out_date = models.DateTimeField(null=True, blank=True)

    review_star = models.IntegerField(null=True, blank=True)
    review_comment = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    reply = models.TextField(null=True, blank=True)
    reply_date = models.DateTimeField(null=True, blank=True)
