from django.db import models

# Create your models here.


class Swiped(models.Model):
    MARK = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('superlike', 'superlike'),
    )

    uid = models.IntegerField(verbose_name='用户自身id')
    sid = models.IntegerField(verbose_name='被滑的陌生人')
    mark = models.CharField(choices=MARK, verbose_name='滑动类型', max_length=16)
    time = models.DateTimeField(verbose_name='滑动时间', auto_now_add=True)

    @classmethod
    def like(cls, uid, sid):
        return Swiped.objects.create(uid=uid, sid=sid, mark='like')

    @classmethod
    def dislike(cls, uid, sid):
        return Swiped.objects.create(uid=uid, sid=sid, mark='dislike')

    @classmethod
    def superlike(cls, uid, sid):
        return Swiped.objects.create(uid=uid, sid=sid, mark='superlike')

    @classmethod
    def has_like(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, mark='like').exists()


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = uid1, uid2 if (uid1 < uid2) else (uid2, uid1)
        friendship = cls.objects.create(uid1=uid1, uid2=uid2)
        return friendship

    @classmethod
    def is_friend(cls, uid1, uid2):
        uid1, uid2 = uid1, uid2 if (uid1 < uid2) else (uid2, uid1)
        return Friend.objects.filter(uid1=uid1, uid2=uid2).exists()

    @classmethod
    def delete_friend(cls, uid1, uid2):
        uid1, uid2 = uid1, uid2 if (uid1 < uid2) else (uid2, uid1)
        return Friend.objects.filter(uid1=uid1, uid2=uid2).delete()