from django.db import model
from django.conf import settings
from django.contrib.auth import get_user_model
from movies.models import *

User = get_user_model()
# private :: diary -> only self
class Diary(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    # 사용자가 본 날
    watched_at = models.DateField()
    # 사용자가 등록한 이미지 
    # db에 존재하는 영화 img를 사용할 수도 있게 해야하는데,
    # 검색한 이미지를 잘 추가 할 수 있을까? 생각해봐야한다.
    # 이미지 여러가지 할지 의논필
    image = models.ImageField(upload_to=user_path)
    main_image = models.ImageField(bank=True) # 필수입력 해제
    # 등록한 사용자
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
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
    movies = models.ManyToManyField("movies.Movie", related_name="collections")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=150)
    content = models.TextField()
    # 사용자가 등록한 이미지 
    # db에 존재하는 영화 img를 사용할 수도 있게 해야하는데,
    # 검색한 이미지를 잘 추가 할 수 있을까? 생각해봐야한다.

    # 등록한 사용자
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



