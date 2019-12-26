from django.db import models


class Vip(models.Model):
    level = models.IntegerField(default=0, verbose_name='vip等级')
    price = models.FloatField(verbose_name='vip价格')
    name = models.CharField(verbose_name='vip名称', max_length=128)

    def __str__(self):
        return f'<Vip {self.level}>'

    def has_perm(self, perm_name):
        # 先取出当前vip所具有的所有权限
        relations = VipPermRelation.objects.filter(vip_id=self.id).only('perm_id')
        perm_id_list = [i.perm_id for i in relations]
        perms = Permission.objects.filter(id__in=perm_id_list)
        for perm in perms:
            if perm_name == perm.name:
                return True
        return False


class Permission(models.Model):
    name = models.CharField(verbose_name='权限名称', max_length=128)
    description = models.TextField(verbose_name='权限描述')

    def __str__(self):
        return f'<Perm {self.name}>'


class VipPermRelation(models.Model):
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()