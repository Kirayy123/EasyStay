
import random
from django.http import HttpResponse
from django.shortcuts import render


from EasyStay.form import UserLoginForm, ManagerLoginForm

from EasyStay.cbvs import CreateUserView, CreateManagerView
from EasyStay.models import user, hotelmanager, hotel, room, roomtype


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

def hotel_details(request,id):
    context_hotel = {}
    try: 
        hoteldisplayed = hotel.objects.get(hotel_id=id)
        roomsdisplayed = roomtype.objects.filter(hotel=hoteldisplayed)
        #splits the ',' separated list of hotel features in the database field into an array of each seperate item
        context_hotel['Facility'] = filter(None,hoteldisplayed.facility.split(','))
        context_hotel['hotel'] = hoteldisplayed
        context_hotel['rooms'] = roomsdisplayed
        #turns the hotel rating into an iterable so that the star symbols are repeated based on the rating
        context_hotel['rating'] = range(hoteldisplayed.star)
    except hotel.DoesNotExist:
        context_hotel['hotel'] = None
        context_hotel['rooms'] = None

    return render(request, 'hotels/hotel_details.html', context_hotel)

#redirects to a page for random hotel in the database
def show_random_hotel(request):
    hotels = hotel.objects.all()
    randHotel = random.choice(hotels)
    return hotel_details(request, randHotel.hotel_id)



def search_rst(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        print('location:',location)
        rsts = hotel.objects.filter(position__icontains=location).all()
        return render(request, 'search_rst.html', locals())


