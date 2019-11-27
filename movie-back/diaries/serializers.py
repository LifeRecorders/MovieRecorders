from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

# 이거면 된다. settings.py에 등록되어서 사용
User = get_user_model()