from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import *
from .models import User

User = get_user_model()

'''
post요청으로 들어온다.

login
email
pwd

signup
username
email
pwd
'''

# 회원가입
@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_signup(request):
    serializer = UserCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        # print(serializer.data)
        return Response({'message': '회원가입이 성공적으로 완료되었습니다.'})


@api_view(['GET'])
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = UserDetailSerializer(instance=user)
    return Response(serializer.data)