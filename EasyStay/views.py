
from django.http import HttpResponse
from django.shortcuts import render


from EasyStay.form import UserLoginForm, ManagerLoginForm

from EasyStay.cbvs import CreateUserView, CreateManagerView
from EasyStay.models import user, hotelmanager


def login_home(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            object_set = user.objects.filter(email=email)
            if object_set.count() == 0:
                form.add_error("email", "The email have not registered.")
            else:
                thisuser = object_set[0]
                if form.cleaned_data["password"] != thisuser.password:
                    form.add_error("password", "Password Incorrect.")
                else:
                    request.session['email'] = email
                    request.session['id'] = thisuser.id
                    # login successfully
                    temp_res = "Hello，%s" % email
                    return HttpResponse(temp_res)
        # verify error
        return render(request, 'login/user_login.html', {'form': form})

    else:
        # get userID from url
        user_id = request.GET.get('uid')
        context = {'form': UserLoginForm(initial={'uid': user_id})} if user_id else {'form': UserLoginForm()}
        context['user_id'] = user_id
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')
        return render(request, 'login/user_login.html', context)


def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            object_set = hotelmanager.objects.filter(email=email)
            if object_set.count() == 0:
                form.add_error("email", "this email has not been registered.")
            else:
                thisuser = object_set[0]
                if form.cleaned_data["password"] != thisuser.password:
                    form.add_error("password", "Password not correct!")
                else:
                    request.session['email'] = email
                    request.session['id'] = thisuser.id
                    # successful login
                    temp_res = "hello, %s" % email
                    return HttpResponse(temp_res)
            return render(request, 'login/manager_login.html', {'form': form})
    else:
        user_id = request.GET.get('uid')
        context = {'form': ManagerLoginForm(initial={'uid': user_id})} if user_id else {'form': ManagerLoginForm()}
        context['user_id'] = user_id

        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')
        return render(request, 'login/manager_login.html', context)


def user_register(request):
    func = CreateUserView.as_view()
    return func(request)


def manager_register(request):
    func = CreateManagerView.as_view()
    return func(request)


def search_home(request):
    return render(request, 'search/home.html')

def hotel_details(request):
    return render(request, 'hotels/hoteldetails/html')
