from django.db import models
from django.utils import timezone

# Create your models here.

class user(models.Model):
    user_id = models.CharField(max_length=10, default='default_user_id')
    username = models.CharField(max_length=50, default='default_username')
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50, default='+0000000000')
    password = models.CharField(max_length=50)


class hotelmanager(models.Model):
    hotel_name = models.CharField(max_length=50, default='default_hotel_name')
    manage_id = models.CharField(max_length=10, default='default_manage_id')
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50, default='+0000000000')
    password = models.CharField(max_length=50)
    position = models.CharField(max_length=50, default='Manager')


class hotel(models.Model):
    manager = models.ForeignKey(hotelmanager, on_delete=models.CASCADE)
    hotel_id = models.CharField(max_length=10, default='default_hotel_id')
    name = models.CharField(max_length=100, default='default_hotel_name')
    city = models.CharField(max_length=50, default='default_city')
    location = models.CharField(max_length=255, default='default_location')
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50, default='+0000000000')
    star = models.IntegerField(default=3)
    description = models.TextField(default='No description provided.')
    facility = models.TextField(default='Basic facilities.')


class roomtype(models.Model):
    type = models.CharField(max_length=50, default='Standard')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)
    facility = models.TextField(default='Basic room facilities.')


class room(models.Model):
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    type = models.ForeignKey(roomtype, on_delete=models.CASCADE)
    number = models.CharField(max_length=10, default='001')
    availability = models.BooleanField(default=True)  # True for available, False for unavailable


class booking(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    room_number = models.ForeignKey(room, on_delete=models.CASCADE)
    ref_num = models.CharField(max_length=50, default='REF0001')
    date = models.DateTimeField(default=timezone.now)
    check_in_date = models.DateTimeField(default=timezone.now)
    check_out_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    status = models.TextField(default='1')  # '1' for wait check-in
    review_star = models.IntegerField(default=5)
    review_comment = models.TextField(default='No comment.')
    review_date = models.DateTimeField(default=timezone.now)


# Uncomment and adjust default values as needed for your application logic
# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
#     star = models.IntegerField(default=5)
#     comment = models.TextField(default='No comment.')
#     date = models.DateTimeField(default=timezone.now)