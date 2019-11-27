from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('users/<int:user_id>/', views.user_detail),
    path('register/', views.user_signup, name='user_signup')
]