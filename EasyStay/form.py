import re

from django import forms

from EasyStay.models import user, hotelmanager, hotel, roomtype, room, booking

'''__User Login Form__'''


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)


'''__Manager Login Form__'''


class ManagerLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)


'''__ Password Check Function __'''


def checkpassword(self, password, confirm_password):
    if password is None:
        return
    if len(password) < 8:  # len longer than 8
        self.add_error('password', 'Your password is too short.')
    elif not any(char.isdigit() for char in password):  # contain digit
        self.add_error('password', 'Your should contain at least one digit.')
    elif not any(char.isupper() for char in password):  # contain uppsercase
        self.add_error('password', 'Your password should contain at least one uppercase letter.')
    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # contain symbol
        self.add_error('password', 'Your password should contain at least one symbol.')
    elif confirm_password != password:  # the confirmed password should be the same as the input password
        self.add_error('confirm_password', 'Password does not match.')


'''__ User Register Form__'''


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password")
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
        help_text="Your password must be at least 8 characters long, \n"
                  "contain at least one uppercase, one digit and one special character")

    class Meta:
        model = user
        fields = ('username',
                  'email',
                  'phone',
                  'password',
                  'confirm_password')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = ''
        self.fields['phone'].initial = ''

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        checkpassword(self, password, confirm_password)


'''__ Manager Register Form __'''


class ManagerRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password",
                               help_text="Your password must be at least 8 characters long, \n"
                                         "contain at least one uppercase, one digit and one special character")

    class Meta:
        model = hotelmanager
        fields = ('email',
                  'phone',
                  'password',
                  'confirm_password')

    def __init__(self, *args, **kwargs):
        super(ManagerRegisterForm, self).__init__(*args, **kwargs)
        self.fields['phone'].initial = ''

    def clean(self):
        cleaned_data = super(ManagerRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        checkpassword(self, password, confirm_password)


'''__ Manager Information Form __'''


class ManagerInfoForm(ManagerRegisterForm):
    class Meta:
        model = hotelmanager
        fields = ['manage_id', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super(ManagerInfoForm, self).__init__(*args, **kwargs)
        # read-only in the profile page
        self.fields['manage_id'].disabled = True
        self.fields['email'].disabled = True
        self.fields['phone'].disabled = True

        if 'confirm_password' in self.fields:
            del self.fields['confirm_password']
        if 'password' in self.fields:
            del self.fields['password']

        new_order = ['manage_id', 'email', 'phone']
        self.order_fields(new_order)


'''__ Manager Information Edition Form __'''


class ManagerInfoEditForm(ManagerRegisterForm):
    class Meta:
        model = hotelmanager
        fields = ['manage_id', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super(ManagerInfoEditForm, self).__init__(*args, **kwargs)
        # read-only, the manager number can not be modified
        self.fields['manage_id'].disabled = True

        if 'confirm_password' in self.fields:
            del self.fields['confirm_password']
        if 'password' in self.fields:
            del self.fields['password']

        new_order = ['manage_id', 'email', 'phone']
        self.order_fields(new_order)


'''__ The choices can be choose in facility filed __'''
FACILITY_CHOICES = [
    ('Wi-Fi', 'Wi-Fi'),
    ('TV', 'TV'),
    ('Air conditioning', 'Air conditioning'),
    ('Private Bathroom', 'Private Bathroom'),
    ('Room Service', 'Room service'),
    ('Balcony', 'Balcony'),
    ('Sea View', 'Sea view'),
    ('Parking', 'Parking'),
    ('Lift', 'Lift'),
    ('Swimming Pool', 'Swimming Pool'),
    ('Gym', 'Gym'),
    ('Spa', 'Spa'),
    ('Restaurant', 'Restaurant'),
    ('Breakfast', 'Breakfast'),
    ('Bar', 'Bar'),
    ('Pets Friendly', 'Pets friendly'),
    ('Non-smoking Rooms', 'Non-smoking Rooms'),
    ('Conference Room', 'Conference Room'),
    ('Facilities for disabled guests', 'Facilities for disabled guests')]

'''__ Hotel Information Form __'''


class HotelInfoForm(forms.ModelForm):
    facility = forms.MultipleChoiceField(
        choices=FACILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = hotel
        fields = '__all__'
        exclude = ['manager', 'hotel_id', 'star']

    def __init__(self, *args, **kwargs):
        super(HotelInfoForm, self).__init__(*args, **kwargs)
        self.fields['location'].initial = ''
        self.fields['phone'].initial = ''
        self.fields['description'].initial = ''
        widgets = {
            'image': forms.FileInput(),
        }


'''__ Hotel Edition Form __'''


class HotelEditForm(HotelInfoForm):
    class Meta:
        model = hotel
        fields = '__all__'
        exclude = ['manager', 'star']

    def __init__(self, *args, **kwargs):
        super(HotelEditForm, self).__init__(*args, **kwargs)
        # read-only, the hotel number can not be modified
        self.fields['hotel_id'].disabled = True
        # reorder the information sequence that displayed
        new_order = ['hotel_id'] + \
                    [field for field in self.fields if field not in ['manager', 'hotel_id', 'star']]
        self.order_fields(new_order)


'''__ Room Type Form __'''


class RoomTypeForm(forms.ModelForm):
    facility = forms.MultipleChoiceField(
        choices=FACILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = roomtype
        fields = '__all__'
        exclude = ['hotel']

    def __init__(self, *args, **kwargs):
        super(RoomTypeForm, self).__init__(*args, **kwargs)
        self.fields['price'].initial = ''
        widgets = {
            'image': forms.FileInput(),
        }
        new_order = ['type', 'price', 'guests']
        self.order_fields(new_order)


'''__ Room Type Edition Form __'''


class RoomTypeEditForm(RoomTypeForm):
    class Meta:
        model = roomtype
        fields = '__all__'
        exclude = ['hotel']


'''__ Room Information Form __'''


class RoomForm(forms.ModelForm):
    class Meta:
        model = room
        fields = '__all__'
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['Room_number'].initial = ''


'''__ Change Password Form __'''


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Old Password (Enter the old password)",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True})
    )
    password = forms.CharField(
        label="New Password (Enter the new password)",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Your password must be at least 8 characters long, \n"
                  "contain at least one uppercase, one digit and one special character"
    )
    confirm_password = forms.CharField(
        label="Confirm New Password (Enter the new password again)",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        checkpassword(self, password, confirm_password)


'''__ Booking Form __'''


class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Check in date')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Check out date')
    reserved_name = forms.CharField(max_length=50)
    reserved_phone = forms.CharField(max_length=50)

    class Meta:
        model = booking
        fields = ['start_date', 'end_date', 'reserved_name', 'reserved_phone']
