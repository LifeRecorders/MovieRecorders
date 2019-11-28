from django.db import models
from django.conf import settings
# 최신 등록된 순으로 보여준다
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

# 다른 파일접근
# from accounts.models import User

class Genre(models.Model):
    genreType = models.CharField(max_length=50)

    def __str__(self):
        return self.genreType


class Movie(models.Model):
    genres = models.ManyToManyField(Genre, related_name='movies')
    # 좋아요 누른 영화
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')
    # 보고싶어요 한 영화
    want_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='want_movies')

    title = models.CharField(max_length=150, blank=True)
    title_en = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    open_date = models.CharField(max_length=100, blank=True)
    # open_date_int = models.DateField(blank=True)
    audience = models.IntegerField(blank=True, null=True)
    naver_poster_url = models.TextField(blank=True)
    naver_big_poster_url = models.TextField(blank=True)
    watch_grade = models.CharField(max_length=50, blank=True)
    running_time = models.CharField(max_length=50, blank=True)
    nation = models.CharField(max_length=100, blank=True)

    company = models.CharField(max_length=150, blank=True)
    # jinheungAPI를 위한 정보
    movieCd = models.TextField(blank=False)
    rank = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    naver_link = models.TextField(blank=False)
    class Meta:
        ordering = ('-pk', )

# 여러 사진을 가져오기 위한 모델
# 1:N
class Scene(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='scenes')
    scene = models.TextField()

# M:N
class Director(models.Model):
    movies = models.ManyToManyField(Movie, related_name='directors')
    # liked_director
    name = models.CharField(max_length=150, blank=True)
    name_en = models.CharField(max_length=150, blank=True)
    img_url = models.TextField(blank=True)

class Actor(models.Model):
    movies = models.ManyToManyField(Movie, related_name='actors', through='Cast')
    # liked_actor
    name = models.CharField(max_length=150, blank=True)
    name_en = models.CharField(max_length=150, blank=True)
    img_url = models.TextField(blank=True)

# 중개모델
class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    cast = models.CharField(max_length=150, blank=True)
    cast_en = models.CharField(max_length=150, blank=True)

# 댓글
# movie_id=3993, user_id=1 로 접근가능
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reviews')
    content = models.CharField(max_length=140)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 대댓글 기능을 위한 스키마
    # 1:N
    parent = models.ForeignKey("movies.Review", on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    class Meta:
        # 최신 댓글부터 보여주도록
        ordering = ('-pk',)
    
    def __str__(self):
        return self.content



    