from django.shortcuts import render, redirect
from web.models import Userinfo
import hashlib
from rbac.service.init_permission import init_permission


def password_md5(origin):
    ha = hashlib.md5()
    ha.update(origin.encode("utf-8"))
    return ha.hexdigest()


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd =request.POST.get('pwd')
    print(Userinfo.objects.all().values_list('name','password'))
    current_user = Userinfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': "用户名或密码错误!"})
    request.session['user_id'] = current_user.pk
    init_permission(request, current_user)
    return render(request, 'index.html')


def logout(request):
    request.session.flush()
    return redirect('/login/')


def index(request):

    return render(request, 'index.html')
