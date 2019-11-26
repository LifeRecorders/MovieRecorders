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
    # 리뷰작성용, 영화 디테일 하단에 누적될 것
    # create api
    path('<int:movie_id>/reviews/', views.review_create),
    # update and delete api
    path('<int:movie_id>/reviews/<int:review_id>/', views.review_update_and_delete),

    # 장르별 영화검색
    path('movies/<str:genretype>/', views.moviewithgenre, name="moviewithgenre"),
]
