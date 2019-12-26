import random

from django.core.cache import cache
from django.db import models

from common import keys


def get(cls, *arg, **kwargs):
    # 只缓存id和pk查询
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk is not None:
        # 先从缓存中查询
        key = keys.OBJECT_KEY % (cls.__name__, pk)
        obj = cache.get(key)
        if obj is None:
            obj = cls.objects.get(*arg, **kwargs)
            cache.set(key, obj, 86400 * 14 * (random.random() + 1))
            return obj
        return obj
    else:
        # 说明不是id和pk查询
        # 调用原来Get
        return cls.objects.get(*arg, **kwargs)


def get_or_create(cls, defaults=None, **kwargs):
    # 只缓存id和pk查询
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk is not None:
        # 先从缓存中查询
        key = keys.OBJECT_KEY % (cls.__name__, pk)
        obj = cache.get(key)
        if obj is None:
            obj = cls.objects.get_or_create(defaults=None, **kwargs)
            cache.set(key, obj, 86400 * 14 * (random.random() + 1))
            return obj
    else:
        # 说明不是id和pk查询
        # 调用原来Get
        cls.objects.get_or_create(defaults=None, **kwargs)


def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    key = keys.OBJECT_KEY % (self.__class__.__name__, self.id)
    cache.set(key, self, 86400 * 14 * (random.random() + 1))
    self._origin_save()


def to_dict(self):
    attr_dict = {}
    for field in self._meta.get_fields():
        attr_dict[field.attname] = getattr(self, field.attname, None)
    return attr_dict


def model_patch():
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    models.Model._origin_save = models.Model.save
    models.Model.save = save
    models.Model.to_dict = to_dict