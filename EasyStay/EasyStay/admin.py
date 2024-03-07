from django.contrib import admin

# Register your models here.
from django.contrib import admin
from EasyStay.models import user, hotelmanager, hotel, roomtype, room, booking

admin.site.register(user)
admin.site.register(hotelmanager)
admin.site.register(hotel)
admin.site.register(roomtype)
admin.site.register(room)
admin.site.register(booking)