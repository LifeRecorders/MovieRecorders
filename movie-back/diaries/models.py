from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from movies.models import *

User = get_user_model()


def user_path(instance, filename): # instance는 Photo 클래스의 객체, filename은 업로드할 파일의 파일이름
    from random import choice   # string으로 나온 결과에서 하나의 문자열만 뽑아냄
    import string               # 무작위 문자열을 뽑아내기 위한 용도
    arr = [choice(string.ascii_letters) for _ in range(8)] # 무작위로 8글자를 뽑아줌
    pid = ''.join(arr)          # 파일 아이디생성
    extension = filename.split('.')[-1] # 파일이름으로부터 확장자명가져오기
    # ex) honux/asfqqwer.png
    return '%s/%s.%s' % (instance.owner.username, pid, extension)

# private :: diary -> only self
# 이미지가 여러가지 1:N이 되도록 설정필요
class Diary(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    # 사용자가 본 날
    watched_at = models.DateField()
    # movies를 등록하던지 image를 등록하던지
    movies = models.ManyToManyField("movies.Movie", related_name='diaries', blank=True)
    image = models.ImageField(upload_to=user_path, blank=True)

    main_image = models.ImageField(blank=True) # 필수입력 해제
    # 등록한 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# public :: collection -> show to other users
# admin 계정으로도 추가할 것
'''
Like 기능이랑 비슷
User 와 Movie 간에 M:N 관계를 맺어서 저장
'''
class Collection(models.Model):
    # 담기(한곳에서만 하면된다.)

    # collection movies에서 add 하기 
    # front 에서 요청(어떤 영화를 선택했는지 pk를 주면 그걸 가지고 생성)이 엮어서 들어올 것, 그러면 그러한 요청을 가지고
    # serializer movies(many=True) => 이런식
    # collection id movie id정보 로 collection만들어서 세이브하고
    # add해주기
    movies = models.ManyToManyField("movies.Movie", related_name='collections')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=150)
    content = models.TextField()
    # 사용자가 등록한 이미지 
    # db에 존재하는 영화 img를 사용할 수도 있게 해야하는데,
    # 검색한 이미지를 잘 추가 할 수 있을까? 생각해봐야한다.

    # 등록한 사용자
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



