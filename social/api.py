import datetime

from django.core.cache import cache
from django.db.models import Q

from common import keys, errors
from lib.http import render_json
from social import logic
from social.models import Swiped, Friend
from swiper import config
from user.models import User


def get_recd_list(request):
    """获取推荐列表"""
    # 注意： 1. 已经滑过不出现
    # 2. 自己不能出现
    # 3. 只推荐符合交友的用户
    user = request.user
    data = logic.get_recd_list(user)
    return render_json(data=data)


def like(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.like(user.id, sid)
    return render_json(data={'match': flag})


def dislike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.dislike(user.id, sid)
    return render_json(data={'unmatch': flag})


def superlike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.superlike(user.id, sid)
    return render_json(data={'match': flag})


def rewind(request):
    """
    每天允许反悔三次，把次数记录redis
    每次执行判断次数是否达到三次
    """
    # 先从缓存中获取当天已经反悔的次数
    user = request.user
    code, data = logic.rewind(user)
    return render_json(code=code, data=data)


def show_friends(request):
    """查看好友列表"""
    # 1 2
    user = request.user
    data = logic.show_friend(user)
    return render_json(data=data)