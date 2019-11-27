from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    # django 는 맞춤 모델을 참조하는 AUTH_USER_MODEL 설정 값을 제공함으로써
    # 기본 User 모델을 오버라이드하도록 할 수 있다.
    # follwers = followings => 친구라고 생각하면 된다.
    # 팔로잉하는 사람들 가져오기 user.followings
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
    # liked_genres = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_users')