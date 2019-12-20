import os

from common import keys
from django.conf import settings

from lib.qiniu import upload_qiniu
from swiper import config


def handle_upload(user, avatar):
    filename = keys.AVATAR_KEY % user.id
    file_path = os.path.join(settings.BASE_DIR, settings.medias, filename)
    with open(file_path, mode='ab') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)

    # 上传到七牛云
    upload_qiniu(user, file_path)
    user.avatar = config.QN_URL + filename
    user.save()