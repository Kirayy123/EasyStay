import ast
import random
import datetime

from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_date

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from EasyStay import models
from EasyStay.form import UserLoginForm, ManagerLoginForm, \
    HotelInfoForm, RoomTypeForm, RoomTypeEditForm, RoomForm, HotelEditForm, ManagerInfoForm, ManagerInfoEditForm, \
    ChangePasswordForm

from EasyStay.cbvs import CreateUserView, CreateManagerView
from EasyStay.models import user, hotelmanager, hotel, roomtype, room, booking

'''__Login__'''


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
                    request.session['manager_id'] = thisuser.manage_id
                    request.session['hotel_registered'] = True
                    # successful login
                    request.session.save()
                    return redirect("manager_home")
            return render(request, 'login/manager_login.html', {'form': form})
    else:
        user_id = request.GET.get('uid')
        context = {'form': ManagerLoginForm(initial={'uid': user_id})} if user_id else {'form': ManagerLoginForm()}
        context['user_id'] = user_id

        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')
        return render(request, 'login/manager_login.html', context)


def manager_logout(request):
    if request.session.get("email", ""):
        del request.session["email"]
    if request.session.get("id", ""):
        del request.session["id"]
    if request.session.get("manager_id", ""):
        del request.session["manager_id"]
    if request.session.get("hotel", ""):
        del request.session["hotel"]
    if request.session.get("from_page", ""):
        del request.session["from_page"]
    return redirect(reverse("manager_login"))


'''__Register__'''


def user_register(request):
    func = CreateUserView.as_view()
    return func(request)


def manager_register(request):
    func = CreateManagerView.as_view()
    return func(request)


'''__manager_HomePage__'''


def manager_home(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    manager = hotelmanager.objects.filter(id=id)[0]
    thishotel = hotel.objects.filter(manager_id=manager)
    object_set = hotel.objects.filter(manager=id)
    if object_set.count() == 0:  # no hotel info,fill hotel info first
        request.session['hotel_registered'] = False
        if request.method == 'POST':
            form = HotelInfoForm(request.POST, request.FILES)

            if form.is_valid():
                hotel_set = set(hotel.objects.all().values_list('hotel_id', flat=True))
                random_id = random.randint(100000000, 999999999)
                while ("H" + str(random_id)) in hotel_set:
                    random_id = random.randint(100000000, 999999999)
                hotel_id = "H" + str(random_id)

                new_hotel = form.save(commit=False)
                new_hotel.hotel_id = hotel_id
                manager_set = hotelmanager.objects.filter(id=id)
                if manager_set.count() == 0:
                    new_hotel.manager = None
                else:
                    new_hotel.manager = manager_set[0]

                new_hotel.save()
                form.save_m2m()
                request.session['hotel_registered'] = True
                return redirect('manager_home')
        else:
            form = HotelInfoForm()

        context = {'form': form,
                   'id': id,
                   'manager_id': manager_id,
                   'from': 'add new'}
        return render(request, 'manager/home_addhotel.html', context)
    else:  # have hotel info
        # calculate room number info
        thishotel = hotel.objects.filter(manager=id)[0]
        room_types = roomtype.objects.filter(hotel=thishotel) if thishotel else []
        today = timezone.now().date()
        booking_count = 0
        total_rooms = 0
        for room_type in room_types:
            rooms = room.objects.filter(type=room_type) if room_type else []
            for aroom in rooms:
                bookings = booking.objects.filter(from_date=today, room_number=aroom)
                if bookings.exists():
                    booking_count += 1
                total_rooms += 1

        available_room = total_rooms - booking_count

        # calculate star
        rooms = room.objects.filter(type__in=room_types)
        bookings = booking.objects.all()
        total_star = 0
        count = 0
        for book in bookings:
            if book.review_star and (book.room_number in rooms):
                total_star += book.review_star
                count += 1
        star = total_star / count if count else 3
        thishotel.star = int(star+0.5)
        thishotel.save()
        if thishotel.facility:
            facility_list = ast.literal_eval(thishotel.facility)
            formatted_facilities = ', '.join(facility_list)
        else:
            formatted_facilities = 'No facilities listed'

        context = {'id': id,
                   'manager_id': manager_id,
                   'manager': manager,
                   'hotel': thishotel,
                   'total_room': total_rooms,
                   'available_room': available_room,
                   'bookings': booking_count,
                   'formatted_facilities': formatted_facilities,
                   'stars': range(thishotel.star),
                   'non_stars': range(5 - thishotel.star)}
        return render(request, 'manager/home.html', context)


def edit_hotel(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    manager = hotelmanager.objects.filter(id=id)[0]
    thishotel = hotel.objects.filter(manager_id=manager).first()
    current_hotel = get_object_or_404(hotel, id=thishotel.id)

    if request.method == 'POST':
        form = HotelEditForm(request.POST, request.FILES, instance=current_hotel)

        if form.is_valid():
            form.save()
            return redirect('manager_home')
    else:
        form = HotelEditForm(instance=current_hotel)

    context = {'form': form,
               'id': id,
               'manager_id': manager_id,
               'from': 'edit'}
    return render(request, 'manager/home_addhotel.html', context)


def manager_profile(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    manager = hotelmanager.objects.filter(id=id)[0]
    thishotel = hotel.objects.filter(manager_id=manager)

    if request.method == 'POST':
        form = ManagerInfoForm(request.POST, request.FILES, instance=manager)

        if form.is_valid():
            form.save()
            return redirect('manager_home')
    else:
        form = ManagerInfoForm(instance=manager)

    context = {'id': id,
               'manager_id': manager_id,
               'manager': manager,
               'hotel': thishotel,
               'form': form}
    return render(request, 'manager/profile.html', context)


def manager_change_pw(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            thisuser = hotelmanager.objects.filter(id=request.user.id)[0]
            old_pw = thisuser.password
            input_old = form.cleaned_data["old_password"]
            input_new1 = form.cleaned_data["new_password1"]
            input_new2 = form.cleaned_data["new_password2"]
            if old_pw != input_old:
                form.add_error("old_password", "Old Password not correct!")
            elif input_new1 != input_new2:
                form.add_error("new_password1", "The Confirmed Password not correct!")
            else:
                thisuser.password = input_new1
                thisuser.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('manager_profile')
    else:
        form = ChangePasswordForm()
    return render(request, 'manager/change_password.html', {'form': form})


def manager_profile_edit(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    manager = hotelmanager.objects.filter(id=id)[0]
    thishotel = hotel.objects.filter(manager_id=manager)

    if request.method == 'POST':
        form = ManagerInfoEditForm(request.POST, request.FILES, instance=manager)

        if form.is_valid():
            form.save()
            return redirect('manager_home')
    else:
        form = ManagerInfoEditForm(instance=manager)

    context = {'id': id,
               'manager_id': manager_id,
               'manager': manager,
               'hotel': thishotel,
               'form': form}
    return render(request, 'manager/profile_edit.html', context)


'''__manager_RoomPage__'''


def manager_room(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    room_types = roomtype.objects.filter(hotel=thishotel) if thishotel else []
    if thishotel:
        room_types = roomtype.objects.filter(hotel=thishotel)
        for room_type in room_types:
            if room_type.facility:
                facility_list = ast.literal_eval(room_type.facility)
                room_type.formatted_facilities = ', '.join(facility_list)
            else:
                room_type.formatted_facilities = 'No facilities listed'
    else:
        room_types = []

    context = {'id': id,
               'manager_id': manager_id,
               'room_types': room_types,
               'hotel': thishotel}
    return render(request, 'manager/room.html', context)


def add_room_type(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, request.FILES)

        if form.is_valid():
            type_name = form.cleaned_data["type"]
            if roomtype.objects.filter(hotel=thishotel, type=type_name).exists():
                form.add_error("type", "This room type has already exist.")
            else:
                new_type = form.save(commit=False)
                new_type.hotel = thishotel
                new_type.save()
                form.save_m2m()
                return redirect('manager_room')
    else:
        form = RoomTypeForm()

    room_types = roomtype.objects.filter(hotel=thishotel) if thishotel else []

    context = {'form': form,
               'id': id,
               'manager_id': manager_id,
               'room_types': room_types,
               'from': 'add new',
               'hotel': thishotel}
    return render(request, 'manager/room_add_type.html', context)


def edit_room_type(request, room_type_id):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    current_roomtype = get_object_or_404(roomtype, id=room_type_id, hotel=thishotel)

    if request.method == 'POST':
        form = RoomTypeEditForm(request.POST, request.FILES, instance=current_roomtype)

        if form.is_valid():
            form.save()
            return redirect('manager_room')
    else:
        form = RoomTypeEditForm(instance=current_roomtype)

    room_types = roomtype.objects.filter(hotel=thishotel) if thishotel else []

    context = {'form': form,
               'id': id,
               'manager_id': manager_id,
               'room_types': room_types,
               'from': 'edit',
               'hotel': thishotel}
    return render(request, 'manager/room_add_type.html', context)


def delete_roomtype(request, room_type_id):
    room_type = get_object_or_404(roomtype, id=room_type_id)
    room_type.delete()
    return redirect('manager_room')


def show_rooms(request, room_type_id):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    thistype = roomtype.objects.filter(id=room_type_id)[0]
    rooms = room.objects.filter(type=thistype) if thistype else []
    context = {'room_type': thistype,
               'from': 'add new',
               'rooms': rooms,
               'id': id,
               'manager_id': manager_id,
               'hotel': thishotel}
    return render(request, 'manager/room_by_type.html', context)


def add_rooms(request, room_type_id):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    thistype = roomtype.objects.filter(id=room_type_id)[0]

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room_number = form.cleaned_data["Room_number"]
            if room.objects.filter(type=thistype, Room_number=room_number).exists():
                form.add_error("Room_number", "This room number has already exist.")
            else:
                new_room = form.save(commit=False)
                new_room.type = thistype
                new_room.save()
                return redirect('show_rooms', room_type_id=thistype.id)
    else:
        form = RoomForm()

    rooms = room.objects.filter(type=thistype) if thistype else []
    context = {'form': form,
               'room_type': thistype,
               'from': 'add new',
               'rooms': rooms,
               'id': id,
               'manager_id': manager_id,
               'hotel': thishotel}
    return render(request, 'manager/room_add_rooms.html', context)


def edit_rooms(request, room_type_id, room_id):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    thistype = roomtype.objects.filter(id=room_type_id)[0]
    current_room = get_object_or_404(room, id=room_id, type=thistype)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=current_room)
        if form.is_valid():
            room_number = form.cleaned_data["Room_number"]
            if room.objects.filter(type=thistype, Room_number=room_number).exclude(id=current_room.id).first():
                form.add_error("Room_number", "This room number has already exist.")
            else:
                form.save()
                return redirect('show_rooms', room_type_id=thistype.id)
    else:
        form = RoomForm(instance=current_room)

    rooms = room.objects.filter(type=thistype) if thistype else []
    context = {'form': form,
               'room_type': thistype,
               'rooms': rooms,
               'id': id,
               'manager_id': manager_id,
               'from': 'edit',
               'hotel': thishotel}
    return render(request, 'manager/room_add_rooms.html', context)


def delete_room(request, room_type_id, room_id):
    thistype = roomtype.objects.filter(id=room_type_id)[0]
    room_type = get_object_or_404(room, id=room_id)
    room_type.delete()
    return redirect('show_rooms', room_type_id=thistype.id)


'''__manager_BookingPage__'''


def booking_list(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    bookings = booking.objects.filter()

    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)

    ####Filter By date/status####
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')

    if start_date:
        # Convert start_date to date object
        start_date = parse_date(start_date)
        print(start_date)
        bookings = bookings.filter(from_date=start_date)

    if end_date:
        # Convert end_date to date object
        end_date = parse_date(end_date)
        bookings = bookings.filter(to_date=end_date)

    if status:
        bookings = bookings.filter(status=status)

    search_query = request.GET.get('search')
    if search_query:
        bookings = bookings.filter(ref_num=search_query)

    bookings = bookings.order_by('status')

    context = {'id': id,
               'manager_id': manager_id,
               'bookings': bookings,
               'hotel': thishotel}
    return render(request, 'manager/booking.html', context)


'''__manager_CheckIn/OutPage__'''


def check_in_list(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]

    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)
    check_in_list = bookings.filter(status=1)

    ####Filter By date####
    start_date = request.GET.get('start_date')
    if start_date:
        # Convert start_date to date object
        start_date = parse_date(start_date)
        print(start_date)
        check_in_list = check_in_list.filter(from_date=start_date)

    search_query = request.GET.get('search')
    if search_query:
        check_in_list = bookings.filter(ref_num=search_query)

    check_in_list = check_in_list.order_by('from_date')

    context = {'id': id,
               'manager_id': manager_id,
               'check_list': check_in_list,
               'action': 'checkin',
               'hotel': thishotel}

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        thisbooking = booking.objects.get(pk=booking_id)
        thisbooking.check_in_date = timezone.now()
        thisbooking.status = 2

        thisroom = room.objects.get(id=thisbooking.room_number.id)
        thisroom.availability = False
        thisroom.save()

        thisbooking.save()
        return redirect('checkin')

    return render(request, 'manager/check_in.html', context)


def check_out_list(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]

    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)
    check_out_list = bookings.filter(status=2)

    ####Filter By date/status####
    end_date = request.GET.get('end_date')
    if end_date:
        # Convert end_date to date object
        end_date = parse_date(end_date)
        check_out_list = check_out_list.filter(to_date=end_date)

    search_query = request.GET.get('search')
    if search_query:
        check_out_list = bookings.filter(ref_num=search_query)

    check_out_list = check_out_list.order_by('to_date')

    context = {'id': id,
               'manager_id': manager_id,
               'check_list': check_out_list,
               'action': 'checkout',
               'hotel': thishotel}

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        thisbooking = booking.objects.get(pk=booking_id)
        thisbooking.check_out_date = timezone.now()
        thisbooking.status = 3
        thisroom = room.objects.get(id=thisbooking.room_number.id)
        thisroom.availability = True
        thisroom.save()
        thisbooking.save()
        return redirect('checkout')

    return render(request, 'manager/check_in.html', context)


############################################################################################
def search_home(request):
    return render(request, 'search/home.html')

def hotel_details(request,hid):
    context_hotel = {}
    try: 
        hoteldisplayed = hotel.objects.filter(id=hid)[0]
        roomsdisplayed = roomtype.objects.filter(hotel=hoteldisplayed)
        context_hotel['Facility'] = hoteldisplayed.facility.split(',')
        context_hotel['hotel'] = hoteldisplayed
        context_hotel['rooms'] = roomsdisplayed
        context_hotel['rating'] = range(hoteldisplayed.star)

    except hotel.DoesNotExist:
        context_hotel['hotel'] = None
        context_hotel['rooms'] = None

    return render(request, 'hotels/hotel_details.html', context_hotel)

def show_random_hotel(request):
    hotels = hotel.objects.all()
    randHotel = random.choice(hotels)
    return hotel_details(request, randHotel.hotel_id)

