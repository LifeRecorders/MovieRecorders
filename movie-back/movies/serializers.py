from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from diaries.serializers import *
from diaries.models import *
from accounts.serializers import *
from accounts.models import *

# 이거면 된다. settings.py에 등록되어서 사용
User = get_user_model()


# collection할때 사용
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'pk', 'genres', 'title', 'title_en', 'description', 
            'open_date', 'audience', 'naver_poster_url', 'naver_big_poster_url', 'watch_grade',
            'nation', 'liked_users', 'company', 'movieCd', 'rank',
            'rating', 'created_at', 'updated_at', 'naver_link', 
            'diaries', 'collections'
        ]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

# search
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'reviews', 'followers']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['pk', 'name', 'name_en', 'img_url']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['pk', 'name', 'name_en', 'img_url']

# 관련된 모든 사진
class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ['scene']

class MovieDetailSerializer(MovieSerializer):
    actors = ActorSerializer(many=True)
    directors = DirectorSerializer(many=True)
    scenes = SceneSerializer(many=True)
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['actors', 'directors', 'scenes']

# review
class ReviewSerializer(serializers.ModelSerializer):
    # 여기에 parent추가하고,
    # views.py에서
    # parent 위에 allow null 처리
    # allow_null
    class Meta:
        model = Review
        fields = [
        'pk', 
        'movie',
        'user',
        'content',
        'score', 
        'created_at', 
        'updated_at',
        'parent', 
        ]

# review 대댓글
class ReviewDetailSerializer(ReviewSerializer):
    children = ReviewSerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = Review
        fields = ReviewSerializer.Meta.fields + ['children', 'user']


class UserDetailSerializer(UserSerializer):
    liked_movies = MovieSerializer(many=True) # user.like_movies.all()
    want_movies = MovieSerializer(many=True)
    liked_reviews = ReviewDetailSerializer(many=True)
    # user가 쓴 diary_set을 가져온다.
    diary_set = DiarySerializer(many=True)
    collection_set = CollectionSerializer(many=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'liked_movies',
            'want_movies',
            'liked_reviews',
            'diary_set',
            'collection_set',
        ]