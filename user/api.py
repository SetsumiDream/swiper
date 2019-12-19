from django.shortcuts import render
from django.http import JsonResponse

from lib.sms import send_sms
from common import errors
from lib.http import render_json


# Create your views here.


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