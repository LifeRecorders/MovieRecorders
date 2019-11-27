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

# 전체조회
@api_view(['GET'])
def genres_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movies_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# token없이도 가능하도록 한다.
@permission_classes((AllowAny, ))
def search_data(request):
    # reqeust를 확인 
    # dict로 받음
    searchKeyword = request.GET.get('q')
    if searchKeyword == '':
        context = {}
        return JsonResponse(context)
    else:
        # 영어로 검색시도 해야한다.
        movie = ''
        director = ''
        actor = ''
        user = ''
        scene = ''
        results = {}
        if Movie.objects.filter(title__icontains=searchKeyword).exists() == True:
            movie = Movie.objects.filter(title__icontains=searchKeyword)
            # for m in movie:
            #     scenes = Scene.objects.filter(movie_id=m.id)
            #     print(scenes)
        if Director.objects.filter(name__icontains=searchKeyword).exists() == True:
            director = Director.objects.filter(name__icontains=searchKeyword)
        if Actor.objects.filter(name__icontains=searchKeyword).exists() == True:
            actor = Actor.objects.filter(name__icontains=searchKeyword)
        if User.objects.filter(username__icontains=searchKeyword).exists() == True:
            user = User.objects.filter(username__icontains=searchKeyword)
        userserializer = UserSerializer(user, many=True)
        actorserializer = ActorSerializer(actor, many=True)
        directorserializer = DirectorSerializer(director, many=True)
        moviedetailserializer = MovieDetailSerializer(movie, many=True)

        results['user'] = userserializer.data
        results['movie'] = moviedetailserializer.data
        results['director'] = directorserializer.data
        results['actor'] = actorserializer.data
        
        return Response(results)


# review
# get요청으로 들어오고 movie_id -> 댓글 주면된다.

@api_view(['GET'])
@permission_classes((AllowAny, ))
def review_detail(request):
    if request.method == 'GET':
        movie_id = request.GET.get('movieId')
        movie = Movie.objects.get(pk=movie_id)
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

@api_view(['POST', 'PUT', 'DELETE'])
def reviews_create_update_delete(request):
    if request.method == 'POST':
        # nothing
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie_id=movie_id)
            return Response(serializer.data)

    if request.method == 'PUT':
        # movie_id
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Review has been updated!'})

    if request.method == 'DELETE':
        # movie_id, review_id
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return Response({'message':'Review has been deleted!'})


@api_view(['GET'])
def moviewithgenre(request, genretype):
    genres = Genre.objects.get(genreType=genretype)
    movies = Movie.objects.filter(genres=genres.id)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)