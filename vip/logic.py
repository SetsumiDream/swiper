

# 判断当前用户是否具有某个权限，就是判断当前用户所在的vip等级有没有这个权限
from common import errors


def need_perm(perm_name):
    def wrapper(view_func):
        def inner(request, *args, **kwargs):
            user = request.user
            if user.vip.has_perm(perm_name):
                result = view_func(*args, **kwargs)
                return result
            else:
                raise errors.PermissionDenied
        return inner
    return wrapper
