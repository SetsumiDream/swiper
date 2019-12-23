from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 白名单，如果在白名单内，直接返回
        # print(request.path)
        white_list = ['/api/user/submit/phone/',
                      '/api/user/submit/vcode/']
        if request.path in white_list:
            return None
        # 判断request的session中是否存在uid
        # 不存在就提示没登陆
        uid = request.session.get('uid')
        # print(uid)
        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED, data='请登录')
        # 如果登录了， 就把user写入request
        user = User.objects.get(id=uid)
        request.user = user

