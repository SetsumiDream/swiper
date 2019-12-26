from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User
from common.errors import LogicErr


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
        print(User.get(id=uid))
        user = User.get(id=uid)
        request.user = user


class LogicErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # 只捕获逻辑错误
        if isinstance(exception, LogicErr):
            return render_json(exception.code, exception.data)
        return None


