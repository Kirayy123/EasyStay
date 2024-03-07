from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from EasyStay.form import UserRegisterForm, ManagerRegisterForm, HotelInfoForm, RoomTypeEditForm

from EasyStay.models import user, hotelmanager
import random

'''__User Register View__'''
'''
Get a random user number starting with U, and check with no duplicate
'''
class CreateUserView(CreateView):
    model = user
    form_class = UserRegisterForm
    template_name = "login/user_register.html"
    success_url = "login"

    def form_valid(self, form):
        # order_by is increasing ，-number mean decreasing order
        user_set = set(user.objects.all().values_list('user_id', flat=True))
        random_id = random.randint(100000000, 999999999)
        while ("U" + str(random_id)) in user_set:
            random_id = random.randint(100000000, 999999999)

        user_id = "U" + str(random_id)

        new_user = form.save(commit=False)
        new_user.user_id = user_id
        new_user.save()
        form.save_m2m()

        self.object = new_user

        #After register, jump back to login page and show the user number, that can login with email
        return redirect(reverse('login') + f'?uid={user_id}&from_url=user_register')

'''Manager Register View__'''
'''
Get a random manager number starting with M, and check with no duplicate
Also auto generate a hotel number starting with H
The manager must fill the hotel information when first login to the web, and then they can manager their hotel
'''
class CreateManagerView(CreateView):
    model = hotelmanager
    form_class = ManagerRegisterForm
    template_name = "login/manager_register.html"
    success_url = reverse_lazy('manager_login')

    def form_valid(self, form):
        manager_set = set(hotelmanager.objects.all().values_list('manage_id', flat=True))
        random_id = random.randint(100000000, 999999999)
        while ("M" + str(random_id)) in manager_set:
            random_id = random.randint(100000000, 999999999)

        manage_id = "M" + str(random_id)
        hotel_id = "H" + str(random_id)

        new_manager = form.save(commit=False)
        new_manager.manage_id = manage_id
        new_manager.hotel_id=hotel_id
        new_manager.save()
        form.save_m2m()

        self.object = new_manager
        # After register, jump back to login page and show the manager number, and can login with email
        return redirect(reverse('manager_login') + f'?uid={manage_id}&from_url=manager_register')
