from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from EasyStay.form import UserRegisterForm, ManagerRegisterForm

from EasyStay.models import user, hotelmanager
import random


class CreateUserView(CreateView):
    model = user
    form_class = UserRegisterForm
    # fields = "__all__"
    template_name = "login/user_register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # order_by默认升序排列，number前的负号表示降序排列
        user_set = set(user.objects.all().values_list('user_id', flat=True))
        random_id = random.randint(100000000, 999999999)
        while ("U" + str(random_id)) in user_set:
            random_id = random.randint(100000000, 999999999)

        user_id = "U" + str(random_id)

        # Create, but don't save the new student instance.
        new_user = form.save(commit=False)
        # Modify the student
        new_user.user_id = user_id
        # Save the new instance.
        new_user.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_user

        messages.success(self.request, f"Register Successfully, Your Account Number is: {user_id}")

        # Redirect with parameters
        return redirect(f"{self.success_url}?uid={user_id}&from_url=user_register")

class CreateManagerView(CreateView):
    model = hotelmanager
    form_class = ManagerRegisterForm
    # fields = "__all__"
    template_name = "login/manager_register.html"
    success_url = reverse_lazy('manager_login')

    def form_valid(self, form):
        # order_by默认升序排列，number前的负号表示降序排列
        manager_set = set(hotelmanager.objects.all().values_list('manage_id', flat=True))
        random_id = random.randint(100000000, 999999999)
        while ("M" + str(random_id)) in manager_set:
            random_id = random.randint(100000000, 999999999)

        manage_id = "M" + str(random_id)
        hotel_id = "H" + str(random_id)

        # Create, but don't save the new student instance.
        new_manager = form.save(commit=False)
        # Modify the student
        new_manager.manage_id = manage_id
        new_manager.hotel_id=hotel_id
        # Save the new instance.
        new_manager.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_manager

        # from_url = "manager_register"
        # base_url = reverse(self.get_success_url())
        # return redirect(base_url + '?uid=%s&from_url=%s' % (manage_id, from_url))

        messages.success(self.request, f"Register Successfully, Your Account Number is: {manage_id}")

        # Redirect with parameters
        return redirect(f"{self.success_url}?uid={manage_id}&from_url=manager_register")