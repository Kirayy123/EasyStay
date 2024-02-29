from EasyStay import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_home, name="login"),
    path('login/manager', views.manager_login, name="manager_login"),
    path('Uregister/', views.user_register, name="user_register"),
    path('Mregister/', views.manager_register, name="manager_register"),
    path('search/', views.search_home, name="search_home"),
    path('hotels/hoteldetails/', views.hotel_details, name="hotel_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)