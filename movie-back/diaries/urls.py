from django.urls import path 
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


app_name = 'diaries'
urlpatterns = [
    path('', views.index, name='index'),
    # True or False 반환
    # diaries/diaries/
    path('diaries/', views.diaries, name='diaries'),
    # diary정보 get, put, delete, post
    # diaries/diaries/diaries_create_update_delete/
    path('diaries/diaries_create_update_delete/', views.diaries_create_update_delete, name='diaries_create_update_delete'),
    path('collections/', views.collections, name='collections'),
    path('collections/collections_create_update_delete/', views.collections_create_update_delete, name='collections_create_update_delete'), 
]

# 어떤 URL을 정적으로 추가할래? > MEDIA_URL을 static 파일 경로로 추가
# 실제 파일은 어디에 있는데? > MEDIA_ROOT 경로내의 파일을 static 파일로 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)