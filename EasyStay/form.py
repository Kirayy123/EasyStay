from django import forms

from EasyStay.models import user, hotelmanager, hotel, roomtype, room


# ___Login
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)


class ManagerLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)


# ___Register
class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

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
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')


class ManagerRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

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
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')


class ManagerInfoForm(ManagerRegisterForm):
    class Meta:
        model = hotelmanager
        fields = ['manage_id', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super(ManagerInfoForm, self).__init__(*args, **kwargs)
        # read-only
        self.fields['manage_id'].disabled = True
        self.fields['email'].disabled = True
        self.fields['phone'].disabled = True

        if 'confirm_password' in self.fields:
            del self.fields['confirm_password']
        if 'password' in self.fields:
            del self.fields['password']

        new_order = ['manage_id', 'email', 'phone']
        self.order_fields(new_order)


class ManagerInfoEditForm(ManagerRegisterForm):
    class Meta:
        model = hotelmanager
        fields = '__all__'
        exclude = ['hotel_name', 'password']

    def __init__(self, *args, **kwargs):
        super(ManagerInfoEditForm, self).__init__(*args, **kwargs)
        # read-only
        self.fields['manage_id'].disabled = True

        if 'confirm_password' in self.fields:
            del self.fields['confirm_password']
        if 'password' in self.fields:
            del self.fields['password']

        new_order = ['manage_id', 'email', 'phone', 'password', 'confirm_password']
        self.order_fields(new_order)


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


class HotelEditForm(HotelInfoForm):
    class Meta:
        model = hotel
        fields = '__all__'
        exclude = ['manager','star']

    def __init__(self, *args, **kwargs):
        super(HotelEditForm, self).__init__(*args, **kwargs)
        # read-only
        self.fields['hotel_id'].disabled = True

        new_order = ['hotel_id'] + \
                    [field for field in self.fields if field not in ['manager', 'hotel_id', 'star']]
        self.order_fields(new_order)


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


class RoomTypeEditForm(RoomTypeForm):
    class Meta:
        model = roomtype
        fields = '__all__'
        exclude = ['hotel']


class RoomForm(forms.ModelForm):
    class Meta:
        model = room
        fields = '__all__'
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['Room_number'].initial = ''


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Old Password (Enter the old password)",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True})
    )
    new_password1 = forms.CharField(
        label="New Password (Enter the new password)",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password (Enter the new password again)",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )