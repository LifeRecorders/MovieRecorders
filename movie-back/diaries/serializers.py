from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

# 이거면 된다. settings.py에 등록되어서 사용
User = get_user_model()



# Diary
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = [
            'title', 'content', 'watched_at',
            'movies', 'image', 'main_image', 'owner',
            'created_at', 'updated_at'
            ]



# Collection
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


