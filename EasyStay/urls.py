from django.conf.urls.static import static

from AATP import settings
from EasyStay import views
from django.urls import path

urlpatterns = [
                  # LoginPage
                  path('login/', views.login_home, name="login"),
                  path('login/manager', views.manager_login, name="manager_login"),
                  path('logout/', views.logout, name="logout"),
                  path('Uregister/', views.user_register, name="user_register"),
                  path('Mregister/', views.manager_register, name="manager_register"),

                  # ManagerPage
                  path('manager/', views.manager_home, name="manager_home"),
                  path('manager/updatehotel', views.edit_hotel, name="edit_hotel"),

                  path('manager/room', views.manager_room, name="manager_room"),
                  path('manager/room/addtype', views.add_room_type, name="add_room_type"),
                  path('manager/room/update/<int:room_type_id>/', views.edit_room_type, name="update_room_type"),
                  path('manager/room/delete/<int:room_type_id>/', views.delete_roomtype, name="delete_room_type"),

                  path('manager/room/<int:room_type_id>/', views.show_rooms, name="show_rooms"),
                  path('manager/room/<int:room_type_id>/addrooms', views.add_rooms, name="add_rooms"),
                  path('manager/room/<int:room_type_id>/update/<int:room_id>', views.edit_rooms, name="update_rooms"),
                  path('manager/room/<int:room_type_id>/delete/<int:room_id>', views.delete_room, name="delete_rooms"),

                  path('manager/booking', views.booking_list, name="bookings"),

                  path('manager/review', views.review_list, name="review"),
                  path('manager/reply_review/<int:id>/', views.reply_to_review, name="reply_to_review"),
                  path('manager/review_filter', views.review_filter, name="review_filter"),
                  path('booking_details/<int:booking_id>/', views.get_booking_details, name='get_booking_details'),

                  path('manager/checkin', views.check_in_list, name="checkin"),
                  path('manager/checkout', views.check_out_list, name="checkout"),

                  path('manager/profile', views.manager_profile, name="manager_profile"),
                  path('manager/profile/edit', views.manager_profile_edit, name="manager_profile_edit"),
                  path('manager/profile/change_password', views.manager_change_pw, name="change_password"),

                  path('user/change_password', views.user_change_pw, name="user_change_password"),

                  path('user/booking/<int:type_id>/', views.get_date_booking, name="user_booking"),
                  path('booking/confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
                  path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
                  path('test/', views.search_home, name="test"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
