from django.conf.urls.static import static

from AATP import settings
from EasyStay import views
from django.urls import path

urlpatterns = [
                  # LoginPage
                  path('login/', views.login_home, name="login"),
                  path('login/manager', views.manager_login, name="manager_login"),
                  path('managerlogout/', views.manager_logout, name="manager_logout"),
                  path('Uregister/', views.user_register, name="user_register"),
                  path('Mregister/', views.manager_register, name="manager_register"),

                  # ManagerPage
                  path('manager/', views.manager_home, name="manager_home"),
                  path('manager/updatehotel', views.edit_hotel, name="edit_hotel"),
                  path('manager/room', views.manager_room, name="manager_room"),
                  path('manager/room/addtype', views.add_room_type, name="add_room_type"),
                  path('manager/room/update/<int:room_type_id>/', views.edit_room_type, name="update_room_type"),
                  path('manager/room/<int:room_type_id>/', views.show_rooms, name="show_rooms"),
                  path('manager/room/<int:room_type_id>/addrooms', views.add_rooms, name="add_rooms"),
                  path('manager/room/<int:room_type_id>/update/<int:room_id>', views.edit_rooms, name="update_rooms"),
                  path('manager/booking', views.booking_list, name="bookings"),
                  path('manager/checkin', views.check_in_list, name="checkin"),
                  path('manager/checkout', views.check_out_list, name="checkout"),
                  path('manager/profile', views.manager_profile, name="manager_profile"),
                  path('manager/profile/edit', views.manager_profile_edit, name="manager_profile_edit"),

                  # test
                  path('upload/', views.Test),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
