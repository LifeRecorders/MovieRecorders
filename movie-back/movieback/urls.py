from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    
    # admin 관련
    path('admin/', admin.site.urls),

    # diaries 관련
    path('diaries/', include('diaries.urls')),

    # movies 관련
    path('api/v1/', include('movies.urls')),

    # accounts 관련
    path('accounts/', include('accounts.urls')),
    path('api-token-auth/', obtain_jwt_token),

]
