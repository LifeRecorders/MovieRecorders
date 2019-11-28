from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# from accounts/models.. import User
from .models import *
from movies.models import *
from .serializers import *
import json
import os

User = get_user_model()

def index(request):
    pass

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @permission_classes((AllowAny, ))
def diaries(request):
    user_id = request.GET.get('userId')
    datetime = request.GET.get('datetime') 
    # filter 조건 더 세부적으로 함
    if Diary.objects.filter(user_id=user_id, watched_at=datetime).exists() == True:
        diary = Diary.objects.filter(user_id=user_id)
        return Response(True)   

    elif Diary.objects.filter(user_id=user_id, watched_at=datetime).exists() == False: 
        print(user_id, datetime)
        return Response(False)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def diaries_create_update_delete(request):
    # 다이어리가 없으므로 등록 가능하게 한다
    # user_id, datetime 정보를 받아옴
    # 2019-11-07
    user_id = request.GET.get('userId')
    print(user_id)
    datetime = request.GET.get('datetime') 
    print(datetime)
    # 보여주기
    if request.method == 'GET':
        # 이미 있는 다이어리 정보를 보여준다
        # user_id와도 맞고, datetime과도 동일한 정보를 줘야한다.
        diary = Diary.objects.filter(user_id=user_id, watched_at=datetime)
        serializer = DiarySerializer(diary)
        return Response(serializer.data)

    # 등록
    if request.method == 'POST':
        result = {}
        print(request.data)
        # {'title': '겨울왕국', 'content': '너무 좋았죠', 'watched_at': '2019-11-26', 'movies': 2512, 'user': 2}
        # movies => pk를 가지고 다르게 구성함
        serializer = DiarySerializer(data=request.data, allow_null=True)    
        if serializer.is_valid(raise_exception=True):
            print('-----')
            print(request.data)
            diary = serializer.save(user_id=user_id)
            movie_pk = request.data['movies']
            movie = Movie.objects.get(pk=movie_pk)
            diary.movies.add(movie)
            print(diary.movies.all())
            # print(diary)
            result['serializer'] = serializer.data
            return Response(result)
            
    # 수정 :: 이부분 필요한가?
    if request.method == 'PUT':
        diary = Diary.objects.filter(user_id=user_id, watched_at=datetime)
        serializer = DiarySerializer(data=request.data, instance=diary)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Diary has been updated!'})
    
    # 삭제
    if request.method == 'DELETE':
        diary = Diary.objects.filter(user_id=user_id, watched_at=datetime)
        diary.delete()
        return Response({'message':'Diary has been deleted!'})

# main화면에서 모든 사람들이 그냥 볼 수도 있어야 하므로
@permission_classes((AllowAny, ))
def collections(request):
    collection_id = request.GET.get('collectionId') 
    if Collection.objects.filter(collection_id=collection_id).exists() == True:
        collection = Collection.objects.filter(collection_id=collection_id)
        serializer = CollectionSerializer(collection, many=True)
        return Response(serializer.data)   

@api_view(['POST', 'PUT', 'DELETE'])
def collections_create_update_delete(request):
    # user_id를 보내주면 된다.
    user_id = request.GET.get('userId')
    # collection 작성
    if request.method == 'POST':
        result = {}
        serializer = CollectionSerializer(data=request.data, allow_null=True)
        if serializer.is_valid(raise_exception=True):
            collection = serializer.save(user_id=user_id)
            movies = request.data['movies']
            for movie in movies:
                movie = Movie.objects.get(pk=movie_pk)
                collection.movies.add(movie)
            result['serializer'] = serializer.data
            return Response(result)

    # collection 수정
    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass
