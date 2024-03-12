import ast
import json
import random
import datetime
import populatedata
from EasyStay import mapAPI, weatherAPI


from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_date

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from EasyStay.form import UserLoginForm, ManagerLoginForm, \
    HotelInfoForm, RoomTypeForm, RoomTypeEditForm, RoomForm, HotelEditForm, ManagerInfoForm, ManagerInfoEditForm, \
    ChangePasswordForm, BookingForm

from EasyStay.cbvs import CreateUserView, CreateManagerView
from EasyStay.models import user, hotelmanager, hotel, roomtype, room, booking




'''__Home Page__'''

def index(request):
    return render(request, 'index.html')


'''__Search Results__'''

def search_rst(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        rsts = hotel.objects.filter(Q(city__icontains=location)|
                                    Q(country__icontains=location)).all() 

        for rst in rsts:  # get the star of each review and show in star icon
            rst.stars = range(rst.star)
            rst.non_stars = range(5 - rst.star)
            rst.desc = rst.description
        return render(request, 'search/search_rst.html', locals())



'''__Login__'''
'''
login as guest and direct to guest home page
'''


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
                    # successful login
                    request.session.save()
                    if request.session.get('from') == 'booking':
                        type = request.session.get('type')
                        return redirect('user_booking', type)
                    else:
                        return redirect("index")
        return render(request, 'login/user_login.html', {'form': form})

    else:
        # get userID from url
        user_id = request.GET.get('uid')
        context = {'form': UserLoginForm(initial={'uid': user_id})} if user_id else {'form': UserLoginForm()}
        context['user_id'] = user_id
        if request.GET.get('from_url'):  # get the from url to determine weather it is from register page
            context['from_url'] = request.GET.get('from_url')
        return render(request, 'login/user_login.html', context)


'''
login as manager, and direct to manager home page
'''


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

        if request.GET.get('from_url'):  # this from_url is "manager_login"
            context['from_url'] = request.GET.get('from_url')
        return render(request, 'login/manager_login.html', context)


'''
logout, delete current user information, and direct back to login page
'''


def logout(request):
    request.session.flush()
    return redirect(reverse("index"))

def manager_logout(request):
    request.session.flush()
    return redirect(reverse("manager_login"))

'''__Register__'''
'''
Class-based views for user register
'''


def user_register(request):
    func = CreateUserView.as_view()
    return func(request)


'''
Class-based views for manager register
'''


def manager_register(request):
    func = CreateManagerView.as_view()
    return func(request)


'''__manager_HomePage__'''
'''Show hotel information, hotel image, and room number information,
also contain a navbar as the base of the page.
Every manager can register a hotel,
if no hotel information, should register a hotel first and then manage the hotel.
'''


def manager_home(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    manager = hotelmanager.objects.filter(id=id)[0]
    object_set = hotel.objects.filter(manager=id)
    if object_set.count() == 0:  # no hotel info,fill and registe hotel info first
        request.session['hotel_registered'] = False
        if request.method == 'POST':
            form = HotelInfoForm(request.POST, request.FILES)

            if form.is_valid():  # form to fill hotel information
                hotel_set = set(hotel.objects.all().values_list('hotel_id', flat=True))
                random_id = random.randint(100000000, 999999999)  # random generate a hotel number
                # if the hotel number not exist, set that number to this hotel
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
    else:  # have hotel info, calculate room number info and show it on home page
        thishotel = hotel.objects.filter(manager=id)[0]
        room_types = roomtype.objects.filter(hotel=thishotel) if thishotel else []  # all types of this hotel
        today = timezone.now().date()
        booking_count = 0  # today's number of booking of this hotel
        total_rooms = 0  # total number of room of this hotel
        awaiting_checkin = 0
        for room_type in room_types:
            rooms = room.objects.filter(type=room_type) if room_type else []  # all room of this type
            for aroom in rooms:
                total_rooms += 1
                # filter booking with today and this room [status=1 mean booked today but has not checked in
                bookings = booking.objects.filter(status=1, room_number=aroom, from_date__lte=today)
                if bookings.exists():
                    awaiting_checkin += 1
                    booking_count += 1
                # when the room is checked in, set room.availability to 0
                # so filter the room with customers in with room.availability=0
                if aroom.availability == 0:
                    booking_count += 1

        available_room = total_rooms - booking_count

        # calculate star bby review rating
        rooms = room.objects.filter(type__in=room_types)

        # check whether the booking is expired(the check out date is less than today)
        today = timezone.datetime.today()
        expire_bookings = booking.objects.filter(status__lt=4, to_date__lt=today)
        for abook in expire_bookings:
            abook.status = 4
            abook.save()

        bookings = booking.objects.all()  # get all the bookings of this hotel
        total_star = 0
        count = 0
        for book in bookings:
            # if the customer already reviewed, sum all review star and then calculate average star
            if book.review_star and (book.room_number in rooms):
                total_star += book.review_star
                count += 1
        star = total_star / count if count else 3
        thishotel.star = int(star + 0.5)  # to the nearest int
        thishotel.save()
        if thishotel.facility:  # reform the facility information to display in home page
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
                   'awaiting_checkin': awaiting_checkin,
                   'bookings': booking_count,
                   'formatted_facilities': formatted_facilities,
                   'stars': range(thishotel.star),
                   'non_stars': range(5 - thishotel.star)}
        return render(request, 'manager/home.html', context)


'''__Edit Hotel Information__'''


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


'''__Show Manager Profile__'''


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


'''__Manager Change Password__'''
'''
Only when the old password is right, then you can change your password.
The form will check the new password, at least 8 characters, including at least one digit, symbol, uppercase.
And the confirmed password must be the same as the new password 
'''


def manager_change_pw(request):
    messages.set_level(request, messages.SUCCESS)
    messages.get_messages(request).used = True
    
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            id = request.session.get('id')
            thisuser = hotelmanager.objects.filter(id=id)[0]
            old_pw = thisuser.password
            input_old = form.cleaned_data["old_password"]
            input_new1 = form.cleaned_data["password"]
            if old_pw != input_old:  # check old password
                form.add_error("old_password", "Old Password not correct!")
            else:
                thisuser.password = input_new1
                thisuser.save()
                messages.success(request, 'Password Changed Successfully!')
                return redirect('manager_profile')
    else:
        form = ChangePasswordForm()
    context = {'form': form, 'from': 'manager'}
    return render(request, 'manager/change_password.html', context)


'''__Manager Change Password__'''


def user_change_pw(request):
    messages.set_level(request, messages.SUCCESS)
    messages.get_messages(request).used = True
    
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            id = request.session.get('id')
            thisuser = user.objects.filter(id=id)[0]
            old_pw = thisuser.password
            input_old = form.cleaned_data["old_password"]
            input_new1 = form.cleaned_data["password"]
            if old_pw != input_old:
                form.add_error("old_password", "Old Password not correct!")
            else:
                thisuser.password = input_new1
                thisuser.save()
                messages.success(request, ' Password Changed Successfully!')
                return redirect('user_profile')
    else:
        form = ChangePasswordForm()

    context = {'form': form, 'from': 'user'}
    return render(request, 'user_booking/user_change_pw.html', context)


'''__Edit Manager Profile__'''


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


'''__Manager_RoomPage__'''
'''
Show all room types of the hotel, including basic information of each type
'''


def manager_room(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    if thishotel:
        room_types = roomtype.objects.filter(hotel=thishotel)  # get all types
        for room_type in room_types:
            if room_type.facility:  # reform the facility information of each types
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


'''__Add Room Type__'''


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


'''__edit room type information__'''


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


'''__Delete Room Type__'''


def delete_roomtype(request, room_type_id):
    room_type = get_object_or_404(roomtype, id=room_type_id)
    room_type.delete()
    return redirect('manager_room')


'''__Show Rooms__'''
'''
When click into each type, the page will show all rooms of that type
'''


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


'''__Add Room__'''
'''
In the Room Page, can add rooms, including room number and availability, which will be linked to corresponding room type
and the room number will be checked to avoid duplicate room number
'''


def add_rooms(request, room_type_id):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    thistype = roomtype.objects.filter(id=room_type_id)[0]

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room_number = form.cleaned_data["Room_number"]  # check whether the input room number is exist
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


'''__Edit Room Information__'''


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


'''__Delete Room__'''


def delete_room(request, room_type_id, room_id):
    thistype = roomtype.objects.filter(id=room_type_id)[0]
    room_type = get_object_or_404(room, id=room_id)
    room_type.delete()
    return redirect('show_rooms', room_type_id=thistype.id)


'''__manager_BookingPage__'''
'''
Booking list show all bookings within the hotel
Can filter by satus, date, and can user_booking by reference number
Manager -> Hotel -> Room Type -> Rooms -> Bookings
'''


def booking_list(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]

    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)

    # Filter By date/status#
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    search_query = request.GET.get('search')

    if start_date:
        # check the start date of that booking
        start_date = parse_date(start_date)
        bookings = bookings.filter(from_date=start_date)

    if end_date:
        # check the leave date of that booking
        end_date = parse_date(end_date)
        bookings = bookings.filter(to_date=end_date)

    if status:
        # filter by different status
        bookings = bookings.filter(status=status)

    if search_query:
        # user_booking by the input reference number
        bookings = bookings.filter(Q(ref_num__icontains=search_query) |
                                   Q(reserved_name__icontains=search_query) |
                                   Q(reserved_phone__icontains=search_query))

    bookings = bookings.order_by('status')

    context = {'id': id,
               'manager_id': manager_id,
               'bookings': bookings,
               'hotel': thishotel,
               'search': search_query}
    return render(request, 'manager/booking.html', context)


def get_booking_details(request, booking_id):
    # Make sure that the detail object exists
    detail = booking.objects.filter(id=booking_id).first()
    if detail:
        # Convert the booking object to a dictionary
        # If check_in_date and check_out_date are datetime fields, they need to be formatted
        details = model_to_dict(detail)
        details['room_number'] = detail.room_number.Room_number
        details['room_type'] = detail.room_number.type.type
        details['total_days'] = (detail.to_date-detail.from_date).days
        details['booking_date'] = detail.booking_date.strftime('%Y-%m-%d %H:%M:%S')
        details['bcheck_in_date'] = detail.from_date.strftime('%Y-%m-%d')
        details['bcheck_out_date'] = detail.to_date.strftime('%Y-%m-%d')
        details['check_in_date'] = detail.check_in_date.strftime('%Y-%m-%d %H:%M:%S') if detail.check_in_date else 'have not check in'
        details['check_out_date'] = detail.check_out_date.strftime('%Y-%m-%d %H:%M:%S') if detail.check_out_date else 'have not check in'
        # Serialize the Python dictionary to a JSON string and return an HttpResponse
        return JsonResponse(json.dumps(details, cls=DjangoJSONEncoder), safe=False, content_type='application/json')
    else:
        # If no detail was found, return an empty JSON object
        return JsonResponse({})


'''__Review List__'''
'''
Show all reviews of that hotel, which is the filter the bookings with review
'''


def review_list(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]
    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)

    bookings_with_review = bookings.exclude(review_date__isnull=True)  # the review information is existed
    bookings_with_review.order_by('review_date')

    for bookings in bookings_with_review:  # get the star of each review and show in star icon
        bookings.stars = range(bookings.review_star)
        bookings.non_stars = range(5 - bookings.review_star)

    context = {'id': id,
               'manager_id': manager_id,
               'hotel': thishotel,
               'reviews_bookings': bookings_with_review,
               'room_types': room_types_for_hotel}
    return render(request, 'manager/reviews.html', context)


'''__Filter Review by Room Type__'''


def review_filter(request):
    id = request.session.get('id')
    thishotel = hotel.objects.filter(manager=id)[0]
    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)

    bookings_with_review = bookings.exclude(review_date__isnull=True)
    bookings_with_review.order_by('review_date')

    room_type_query = request.GET.get('room_type')

    if room_type_query:  # Filter by type
        bookings_with_review = bookings_with_review.filter(room_number__type__type=room_type_query)

    for bookings in bookings_with_review:  # get star
        bookings.stars = range(bookings.review_star)
        bookings.non_stars = range(5 - bookings.review_star)

    context = {
        'reviews_bookings': bookings_with_review,
        'room_types': room_types_for_hotel
    }
    return render(request, 'manager/reviews.html', context)


'''__Reply customer Review__'''


def reply_to_review(request, id):
    if request.method == 'POST':
        thisbooking = get_object_or_404(booking, id=id)

        reply_message = request.POST.get('reply')

        if reply_message:
            thisbooking.reply = reply_message
            thisbooking.reply_date = datetime.datetime.now()
            thisbooking.save()
            messages.success(request, 'Your reply was successfully posted.')
        else:
            messages.error(request, 'Your reply cannot be empty.')

        return redirect('review')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('review')


'''__manager_CheckIn/Out Page__'''
'''
status=1(awaiting check in) / status=2(checked in) / status=3(checked out)
can filter by date, user_booking by reference number
can do the check in operation, get the check in time, the status set to 2, room availability set to 0(unavailable)
'''


def check_in_list(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]

    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)
    check_in_list = bookings.filter(status=1)

    start_date = request.GET.get('start_date')
    if start_date:  # Filter By start date
        start_date = parse_date(start_date)
        print(start_date)
        check_in_list = check_in_list.filter(from_date=start_date)

    search_query = request.GET.get('search')
    if search_query:  # user_booking by reference number
        check_in_list = check_in_list.filter(Q(ref_num__icontains=search_query) |
                                             Q(reserved_name__icontains=search_query) |
                                             Q(reserved_phone__icontains=search_query))

    check_in_list = check_in_list.order_by('from_date')

    for abooking in check_in_list:
        total_days = (abooking.to_date - abooking.from_date).days
        abooking.total_days = total_days

    context = {'id': id,
               'manager_id': manager_id,
               'check_list': check_in_list,
               'action': 'checkin',
               'hotel': thishotel}

    if request.method == 'POST':
        # check in operations
        booking_id = request.POST.get('booking_id')
        thisbooking = booking.objects.get(pk=booking_id)
        thisbooking.check_in_date = timezone.now()
        thisbooking.status = 2
        thisbooking.is_paid = 1

        thisroom = room.objects.get(id=thisbooking.room_number.id)
        thisroom.availability = False
        thisroom.save()

        thisbooking.save()
        return redirect('checkin')

    return render(request, 'manager/check_in.html', context)


'''__Check out__'''
'''
get the check out time, the status set to 3, room availability set to 1(available)
'''


def check_out_list(request):
    id = request.session.get('id')
    manager_id = request.session.get('manager_id')
    thishotel = hotel.objects.filter(manager=id)[0]

    room_types_for_hotel = roomtype.objects.filter(hotel=thishotel)
    rooms_for_hotel = room.objects.filter(type__in=room_types_for_hotel)
    bookings = booking.objects.filter(room_number__in=rooms_for_hotel)
    check_out_list = bookings.filter(status=2)

    end_date = request.GET.get('end_date')
    if end_date:  # Filter By end date
        end_date = parse_date(end_date)
        check_out_list = check_out_list.filter(to_date=end_date)

    search_query = request.GET.get('search')
    if search_query:  # user_booking by reference number
        check_out_list = check_out_list.filter(Q(ref_num__icontains=search_query) |
                                               Q(reserved_name__icontains=search_query) |
                                               Q(reserved_phone__icontains=search_query))

    check_out_list = check_out_list.order_by('to_date')

    for abooking in check_out_list:
        total_days = (abooking.to_date - abooking.from_date).days
        abooking.total_days = total_days

    context = {'id': id,
               'manager_id': manager_id,
               'check_list': check_out_list,
               'action': 'checkout',
               'hotel': thishotel}

    if request.method == 'POST':
        # check out operations
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
    type = roomtype.objects.all()[0]
    context = {'type': type}
    return render(request, 'user_booking/home.html', context)


'''__ insert booking information __'''
'''
get input information from user
create a new booking and sture in database
'''


def get_date_booking(request, type_id):
    thistype = roomtype.objects.filter(id=type_id).first()
    rooms_for_type = room.objects.filter(type=thistype)
    user_id = request.session.get('id')

    if user_id == None:
        request.session['from'] = 'booking'
        request.session['type'] = type_id
        request.session.save()
        return redirect('login')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # check whether the select date is valid
            if start_date < end_date:
                total_days = (end_date - start_date).days
                totalprice = thistype.price * total_days
                reserved_name = form.cleaned_data['reserved_name']
                reserved_phone = form.cleaned_data['reserved_phone']

                thisuser = user.objects.get(id=user_id)

                available_room = None
                for aroom in rooms_for_type:
                    # check free rooms within the selected date
                    overlapping_bookings = booking.objects.filter(
                        room_number=aroom,
                        from_date__lt=end_date,  # from date less than end date
                        to_date__gt=start_date  # end date greater than start date
                    ).exists()
                    if not overlapping_bookings:
                        available_room = aroom
                        break

                if available_room:
                    # if have free room, create booking with information
                    booking_set = set(booking.objects.all().values_list('ref_num', flat=True))
                    ref_number = "B" + str(random.randint(100000000, 999999999))

                    while ref_number in booking_set:
                        ref_number = "B" + str(random.randint(100000000, 999999999))

                    new_booking = booking(
                        user=thisuser,
                        room_number=available_room,
                        from_date=start_date,
                        to_date=end_date,
                        total_price=totalprice,
                        ref_num=ref_number,
                        booking_date=timezone.now(),
                        reserved_name=reserved_name,
                        reserved_phone=reserved_phone
                    )
                    new_booking.save()
                    return redirect('confirm_booking', booking_id=new_booking.id)


                else:
                    messages.error(request, 'All rooms are booked for the selected dates.')
                    context = {'form': form, 'type': thistype, 'from': 'no_room'}
                    return render(request, 'user_booking/booking_form.html', context)
            else:
                messages.error(request, 'End date must be after the start date.')
                context = {'form': form, 'type': thistype, 'from': 'date_error'}
                return render(request, 'user_booking/booking_form.html', context)

    else:
        form = BookingForm()

    context = {'form': form, 'type': thistype}
    return render(request, 'user_booking/booking_form.html', context)


'''__ confirm booking __'''
'''
show filled booking information
'''


def confirm_booking(request, booking_id):
    thisbooking = get_object_or_404(booking, id=booking_id)
    start_date = thisbooking.from_date
    end_date = thisbooking.to_date
    total_days = (end_date - start_date).days
    totalprice = thisbooking.room_number.type.price * total_days
    thisbooking.total_price = totalprice
    thisbooking.total_days = total_days
    return render(request, 'user_booking/booking_confirm.html', {'booking': thisbooking})


'''__ cancel current booking process __'''


def cancel_booking(request, booking_id):
    thisbooking = get_object_or_404(booking, id=booking_id)
    typeid = thisbooking.room_number.type.id
    thisbooking.delete()
    return redirect('user_booking', type_id=typeid)







###############################################################################################33
def forgot_password(request):
    if request.method == 'POST':
        request.session['verification_code'] = '1234'
        input_code = request.POST.get('code')

        if input_code == request.session.get('verification_code'):
            request.session['user_email'] = request.POST.get('email')
            request.session['from_url'] = request.GET.get('from_url')
            return render(request, 'login/set_new_password.html')
        else:
            messages.error(request, 'The code entered is incorrect.')

    return render(request, 'login/forgot_password.html')


def set_new_password(request):
    user_email = request.session.get('user_email', None)
    from_url = request.session.get('from_url', None)

    thisuser=0
    if from_url == 'user_login':
        thisuser = user.objects.filter(email=user_email)[0].id
    elif from_url == 'manager_login':
        thisuser = user.objects.filter(email=user_email)[0].id

    if thisuser == 0:
        messages.error(request, 'Email not registed')
        return redirect('forgot_password')

    context = {'user_email': user_email}

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_new_password')
        if len(new_password) < 8:  # len longer than 8
            messages.error( 'Your password is too short.')
        elif not any(char.isdigit() for char in new_password):
            messages.error(request, 'Your should contain at least one digit.')
        elif not any(char.isupper() for char in new_password):
            messages.error(request, 'Your password should contain at least one uppercase letter.')
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
            messages.error(request, 'Your password should contain at least one symbol.')
        elif confirm_password != new_password:
            messages.error(request, 'Password does not match.')
        else:
            thisuser.password=new_password
            thisuser.save()
            messages.success(request, 'Your password has been updated.')
            return redirect('login')

def user_profile(request):
    id = request.session.get('id')
    #if user is logged into their account it will show them their account page
    if id != None:
        u = user.objects.get(id=id)
        reservations = booking.objects.filter(user_id=id)
        context = {}
        context['user'] = u
        context['reservations'] = reservations 
        return render(request, 'user/userProfile.html', context)
    else:
        #else it will direct them to the user login page
        return redirect(login_home)

def booking_management(request,id):
   reservation = booking.objects.get(id=id)
   context = {}
   context['res'] = reservation 
   context['nights'] = round(reservation.total_price / reservation.room_number.type.price, 2)
   context['facilities'] = ast.literal_eval(reservation.room_number.type.facility)

    #used to render the amount of filled starts corresponding with the hotel rating
   context['star'] = range(reservation.room_number.type.hotel.star)
   context['non_star'] = range(5- reservation.room_number.type.hotel.star)

   return render(request, 'user/bookingManagement.html', context)


#Displays the details and room-types of the hotel after being selected in search page
def hotel_details(request,id):
    context_hotel = {}
    try: 
        hoteldisplayed = hotel.objects.get(id=id)
        roomsdisplayed = roomtype.objects.filter(hotel=hoteldisplayed)

        #splits the string of hotel facilities into a list of elements
        if hoteldisplayed.facility:
            formatted_facilities = ast.literal_eval(hoteldisplayed.facility)
        else:
            formatted_facilities = 'No facilities listed'

        #splits the room facilities list up per room type
        roomfacilities = {}
        for r in roomsdisplayed:
            roomfacilities[r] = ast.literal_eval(r.facility)

        context_hotel['Facility'] = formatted_facilities
        context_hotel['hotel'] = hoteldisplayed
        context_hotel['rooms'] = roomsdisplayed
        context_hotel['room_facilities'] = roomfacilities
        context_hotel['rating'] = range(hoteldisplayed.star)
        context_hotel['non_star'] = range(5- hoteldisplayed.star)
        context_hotel['map_api'] = mapAPI.get_key()

        #get latitude and longitude from TomTom API to centre the map 
        coords = mapAPI.getLat_Long(hoteldisplayed.city)
        context_hotel['lat'] = coords['lat']
        context_hotel['long'] = coords['long']

        #use lat & long to get weather information from OpenWeather
        weather = weatherAPI.get_weather(hoteldisplayed.city)
        context_hotel['weather'] = weather['description']
        context_hotel['icon'] = weather['icon']
        context_hotel['temp'] = weather['temp']

    except hotel.DoesNotExist:
        context_hotel['hotel'] = None
        context_hotel['rooms'] = None

    return render(request, 'hotels/hotel_details.html', context_hotel)


def review_booking(request,id):
    if request.method == 'POST':
        thisbooking = get_object_or_404(booking, id=id)

        review_message = request.POST.get('review')
        review_star = request.POST.get('star')

        if review_message:
            thisbooking.review_comment = review_message
            thisbooking.review_star = review_star
            thisbooking.review_date = datetime.datetime.now()
            thisbooking.save()
        #     messages.success(request, 'Your review was successfully posted.')
        # else:
        #     messages.error(request, 'Your review and star cannot be empty.')

        return redirect('booking_management',id)
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('booking_management',id)