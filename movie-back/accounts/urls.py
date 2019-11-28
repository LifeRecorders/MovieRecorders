from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('users/', views.user_detail, name='user_detail'),
    path('register/', views.user_signup, name='user_signup')
]