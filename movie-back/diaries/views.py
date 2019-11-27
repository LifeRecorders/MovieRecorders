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
from .serializers import *
import json
import os

User = get_user_model()

def index(request):
    pass

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny, ))
def diaries(request):
    user_id = request.GET.get('userId')
    datetime = request.GET.get('datetime') 
    if Diary.objects.filter(user_id=user_id).exists() == True:
        diary = Diary.objects.filter(user_id=user_id)
        return Response(True)   
        # if request.method == 'GET':
        #     # 이미 있는 다이어리 정보를 보여준다

        #     pass
            
        # if request.method == 'PUT':
        #     pass

        # if request.method == 'DELETE':
        #     pass

    elif Diary.objects.filter(user_id=user_id).exists() == False: 
        return Response(False)
        # 다이어리가 없으므로 등록 가능하게 한다
        # user_id, datetime 정보를 받아옴
        # 2019-11-07
        # diary = Diary()
        # if request.method == 'POST':
        #     print(user_id, datetime)
        #     serializer = DiarySerializer(data=request.data)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save(user_id=user_id)
        #         return Response(serializer.data)
        #     pass


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def collections(request):
    if request.method == 'GET':
        pass

    # collection 작성
    if request.method == 'POST':
        pass

    # collection 수정
    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass
