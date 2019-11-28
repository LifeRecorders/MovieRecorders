from django.urls import path 
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    # 전체조회
    path('genres/', views.genres_list, name="genres_list"),
    path('movies/', views.movies_list, name="movies_list"),
    # 검색결과용
    path('search/', views.search_data, name="search_data"),
    # 리뷰 보여주기와 작성용, 영화 디테일 하단에 누적될 것
    # detail api create api update and delete api
    path('reviews/', views.review_detail, name="review_detail"), 
    path('reviews_create_update_delete/', views.reviews_create_update_delete, name="reviews_create_update_delete"),
    # 장르별 영화검색
    path('movies/<str:genretype>/', views.moviewithgenre, name="moviewithgenre"),
    
    # 영화 최신순, 평점높고, 관객수 상위 30개
    path('bestmovies/', views.bestmovies, name="bestmovies"),

    # 어떤 유저인지 보내줘야함
    path('myreviews/', views.myreviews, name="myreviews"),

    # 좋아요 기능
    path('like/', views.like, name="like"),

    # 유저가 행동한 모든 정보 / 내가 좋아요한 영화 목록
    path('myinfo/', views.myinfo, name="myinfo"),
]

