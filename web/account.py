from django.shortcuts import render, redirect
from web.models import UserInfo

from rbac.service.init_permission import init_permission


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    current_user = UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': "用户名或密码错误!"})
    request.session['user_info'] = {'id': current_user.id, 'nickname': current_user.nickname}
    request.session['user_id'] = current_user.pk
    init_permission(current_user, request)
    return redirect('/index/')


def logout(request):
    request.session.flush()
    return redirect('/login/')


def index(request):
    return render(request, 'index.html')
