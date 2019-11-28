from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from movies.models import *

# 이거면 된다. settings.py에 등록되어서 사용
User = get_user_model()



# Diary
class DiarySerializer(serializers.ModelSerializer):
    # manytomanyfields는 serializer에 넣지않는다.
    class Meta:
        model = Diary
        fields = [
            'title', 'content', 'watched_at', 'user', 
            ]



# Collection
class CollectionSerializer(serializers.ModelSerializer):
    # manytomanyfields는 serializer에 넣지않는다.
    class Meta:
        model = Collection
        fields = [
            'title', 'content', 'user', 
        ]


