from django import forms
from EasyStay.models import user, hotelmanager

#___Login
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='邮箱', max_length=100)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)

class ManagerLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)

#___Register
class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

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
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = hotelmanager
        fields = ('hotel_name',
                  'email',
                  'phone',
                  'password',
                  'confirm_password')

    def __init__(self, *args, **kwargs):
        super(ManagerRegisterForm, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].initial = ''
        self.fields['phone'].initial = ''

    def clean(self):
        cleaned_data = super(ManagerRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')
