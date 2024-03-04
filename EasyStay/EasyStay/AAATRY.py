from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from EasyStay.form import UserLoginForm, ManagerLoginForm

from EasyStay.cbvs import CreateUserView,CreateManagerView

from EasyStay.models import user,hotelmanager

# Create your views here.

def login_home(request):
    if request.method == 'POST':  # 检查HTTP请求是否为POST方法，这通常表示用户提交了一个表单。
        form = UserLoginForm(data=request.POST)

        if form.is_valid():  # 检查输入信息
            email = form.cleaned_data["email"]
            if len(email) < 5:  # 检查长度
                form.add_error("email", "账号长度必须大于5")
            else:  # 检查是否在DB里面
                object_set = user.objects.filter(email=email)

                if object_set.count() == 0:
                    form.add_error("email", "email 未注册.")
                else:
                    thisuser = object_set[0]
                    if form.cleaned_data["password"] != thisuser.password:
                        form.add_error("password", "密码不正确.")
                    else:
                        request.session['email'] = email
                        request.session['id'] = thisuser.id
                        # successful login
                        #to_url = reverse("search_home", kwargs={'kind': kind})
                        temp_res = "hello, %s" % email
                        return HttpResponse(temp_res)

            return render(request, 'login/user_login.html', {'form': form})
    else:
        form = UserLoginForm()

        return render(request, 'login/user_login.html', {'form': form})