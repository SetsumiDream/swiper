from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

from lib.sms import send_sms
from common import errors
from lib.http import render_json
from common import keys



# Create your views here.
from user.forms import ProfileModelForm
from user.models import User, Profile


def submit_phone(request):
    """提交手机号码，发送验证码"""
    phone = request.POST.get('phone')
    # 发送验证码
    print(phone)
    status, msg = send_sms(phone)

    if not status:
        # return JsonResponse({'code': errors.SMS_ERROR, 'data': '短信发送失败'})
        return render_json(code=errors.SMS_ERROR, data='短信发送失败')
    # 发送成功
    # return JsonResponse({'code': 0, 'data': None})
    return render_json()


def submit_vcode(request):
    """提交短信验证码"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    print(phone)
    print(vcode)
    # 从缓存中取出vcode
    cache_vcode = cache.get(keys.VCODE_KEY % phone)
    print(cache_vcode)
    if vcode == cache_vcode:
        # 验证码正确
        # try:
        #     user = User.objects.get(phonenum=phone)
        # except User.DoesNotExist:
        #     # 说明是注册
        #     user = User.objects.create(phonenum=phone, nickname=phone)
        user, _ = User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        # 验证码错误
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    uid = request.session.get('uid')
    if not uid:
        return render_json(code=errors.LOGIN_REQUIRED, data='请登录')
    user = User.objects.get(id=uid)
    return render_json(data=user.profile.to_dict())


def edit_profile(request):
    # 修改个人资料
    form = ProfileModelForm(request.POST)
    if form.is_valid():
        # 可以接收并保存
        profile = form.save(commit=False)
        uid = request.session.get('uid')
        profile.id = uid
        profile.save()
        return render_json(data=profile.to_dict())
    return render_json(code=errors.PROFILE_ERROR, data=form.errors)















# def user_form(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             nickname = form.cleaned_data['nickname']
#             location = form.cleaned_data['location']
#             sex = form.cleaned_data['sex']
#             age = form.cleaned_data['age']
#             form = form
#             print(nickname, location, sex, age)
#             return render(request, 'user_form.html', locals())
#
#         else:
#             print(form.errors)
#     else:
#         form = UserForm()
#         return render(request, 'user_form.html', {'form': form})



