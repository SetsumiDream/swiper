import datetime

from django.core.cache import cache
from django.db.models import Q

from common import keys, errors
from lib.cache import rds
from lib.http import render_json
from social.models import Swiped, Friend
from swiper import config
from user.models import User


def get_recd_list(user):
    now = datetime.datetime.now()
    max_birth_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age

    # 查询已经被当前用户滑过的人
    swiped_list = Swiped.objects.filter(uid=user.id).only('sid')
    # 取出sid
    sid_list = [s.sid for s in swiped_list]
    sid_list.append(user.id)
    users = User.objects.filter(location=user.profile.location,
                                birth_year__range=[min_birth_year, max_birth_year],
                                sex=user.profile.dating_sex,
                                ).exclude(
        id__in=sid_list)[:20]
    data = [user.to_dict() for user in users]
    return data


def like(uid, sid):
    # 创建一条记录
    Swiped.like(uid, sid)
    # 判断对方是否喜欢
    if Swiped.has_like(uid=sid, sid=uid):
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def dislike(uid, sid):
    # 创建一条记录
    Swiped.dislike(uid, sid)
    # 判断对方是否喜欢
    Friend.delete_friend(uid, sid)
    return True


def superlike(uid, sid):
    # 创建一条记录
    Swiped.dislike(uid, sid)
    # 判断对方是否喜欢
    if Swiped.has_like(uid=sid, sid=uid):
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def rewind(user):
    key = keys.REWIND_KEY % user.id
    cahed_rewinded_times = cache.get(key, 0)
    if cahed_rewinded_times < config.MAX_REWIND:
        try:
            cahed_rewinded_times += 1
            now = datetime.datetime.now()
            left_seconds = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
            cache.set(key, cahed_rewinded_times, timeout=left_seconds)
            record = Swiped.objects.filter(uid=user.id).latest('time')
            Friend.delete_friend(uid1=user.id, uid2=record.sid)

            # 处理排行榜得分
            # if record.mark == 'like':
            #     rds.zincrby(config.HOT_RANK, -config.LIKE_SCORE, keys.HOT_RANK_KEY % record.sid)
            # elif record.mark == 'dislike':
            #     rds.zincrby(config.HOT_RANK, config.DISLIKE_SCORE, keys.HOT_RANK_KEY % record.sid)
            # else:
            #     rds.zincrby(config.HOT_RANK, -config.SUPERLIKE_SCORE, keys.HOT_RANK_KEY % record.sid)

            # 优化，使用模式匹配
            mapping = {
                'like': config.LIKE_SCORE,
                'dislike': config.DISLIKE_SCORE,
                'superlike': config.SUPERLIKE_SCORE
            }
            rds.zincrby(config.HOT_RANK, -mapping[record.mark], keys.HOT_RANK_KEY % record.sid)

            record.delete()
            return True, 'ok'
        except Swiped.DoesNotExist:
            raise errors.NoRecord
    else:
        raise errors.ExceedMaximumRewind


def show_friend(user):
    friends = Friend.objects.filter(Q(uid1=user.id) | Q(uid2=user.id))
    friends_id = []
    for friend in friends:
        if friend.uid1 == user.id:
            friends_id.append(friend.uid2)
        else:
            friends_id.append(friend.uid1)
    users = User.objects.filter(id__in=friends_id)
    data = [user.to_dict() for user in users]
    return data

def get_top_n():
    """
        {
        code: 0,
        data : [
        {id:1,
        rank:1,
        score:100,
        nickname:zhangsan,
        phonenum:186xxxxxxxx.
        ...}
        {id:100,
        rank: 2,
        score: 90,
        nickname ...}
        ]
        }
        """
    # 取出redis中的得分排行
    score_list = rds.zrevrange('Hot-Rank', 0, config.TOP_N, withscores=True)
    print(score_list)
    cleaned_data = [(int(uid), score) for uid, score in score_list]
    uid_list = [uid for uid, _ in cleaned_data]
    # queryset 查询对象的时候,会自动按照对象id的升序排序.
    users = User.objects.filter(id__in=uid_list)
    # 对users排序.
    users = sorted(users, key=lambda user: uid_list.index(user.id))

    # 生成数据
    data = []
    for rank, (_, score), user in zip(range(1, config.TOP_N + 1), cleaned_data, users):
        temp = {}
        temp['rank'] = rank
        temp['score'] = score
        temp.update(user.to_dict())
        data.append(temp)
    return data