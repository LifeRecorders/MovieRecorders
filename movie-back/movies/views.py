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
        serializer = ReviewDetailSerializer(reviews, many=True)
        return Response(serializer.data)



@api_view(['POST', 'PUT', 'DELETE'])
def reviews_create_update_delete(request):
    if request.method == 'POST':
        # 감상평을 남기면 보고싶어요 목록에서 자동삭제하는 로직 필요

        movie_id = request.GET.get('movieId')
        serializer = ReviewSerializer(data=request.data, allow_null=True)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie_id=movie_id)
            return Response(serializer.data)

    if request.method == 'PUT':
        movie_id = request.GET.get('movieId')
        review_id = request.GET.get('reviewId')
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Review has been updated!'})

    if request.method == 'DELETE':
        review_id = request.GET.get('reviewId')
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return Response({'message':'Review has been deleted!'})


@api_view(['GET'])
@permission_classes((AllowAny, ))
def moviewithgenre(request):
    # 번호가 아니라, 이름으로 데이터를 보내줘야 한다.
    genretype = request.GET.get('genretype')
    genres = Genre.objects.get(genreType=genretype)
    movies = Movie.objects.filter(genres=genres.id)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 평가를 남긴 애들 목록 보여주기
@api_view(['GET'])
def myreviews(request):
    user_id = request.GET.get('userId')
    user = User.objects.get(pk=user_id)
    myReviewedMovies = set()
    userReviews = user.reviews.all()
    for review in userReviews:
        mymovie = review.movie
        myReviewedMovies.add(mymovie.title)
    myReviewedMovies = list(myReviewedMovies)
    return Response(myReviewedMovies)

# serializer 사용시 꼭 api_view추가
@api_view(['GET'])
@permission_classes((AllowAny, ))
def bestmovies(request):
    # for 돌리기
    # dictionary=> str-> int datetime lib사용
    # sort 해서 보내기
    
    movies = Movie.objects.all().order_by('rank').order_by('-rating').order_by('-audience').order_by('-open_date')[:30]
    serializer = MovieDetailSerializer(movies, many=True)
    return Response(serializer.data)



# 좋아요 serializer
@api_view(['POST'])
def like(request):
    # movie_pk, user_id 를 받음
    movie_pk = request.GET.get('movieId')
    user_id = request.GET.get('userId')

    movie = get_object_or_404(Movie, pk=movie_pk)
    user = User.objects.get(pk=user_id)

    if user in movie.like_users.all():
        movie.like_users.remove(user)
        liked = False

    else:
        movie.like_users.add(user)
        liked = True

    context = {'liked': liked, 'count': movie.liked_users.count()}
    return JsonResponse(context)


# 보고싶어요 serializer
@api_view(['POST'])
def want(request):
    # movie_pk, user_id 를 받음
    movie_pk = request.GET.get('movieId')
    user_id = request.GET.get('userId')

    movie = get_object_or_404(Movie, pk=movie_pk)
    user = User.objects.get(pk=user_id)

    if user in movie.want_users.all():
        movie.want_users.remove(user)
        wanted = False

    else:
        movie.want_users.add(user)
        wanted = True

    # wanted에 대한 결과와 movie에 대해서 보고싶어요를 한 총 인원 수를 리턴
    context = {'wanted': wanted, 'count': movie.want_users.count()}
    return JsonResponse(context)





@api_view(['GET'])
def myinfo(request):
    # user_id 를 받음, 내가 좋아요한 영화목록 이므로 해당 user_id로 찾음
    # user_id = request.GET.get('userId')
    users = User.objects.all() # 이부분을 특정 user로 받으면 된다.
    serializer = UserDetailSerializer(users, many=True)
    print(serializer)
    return Response(serializer.data)

