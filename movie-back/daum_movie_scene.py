from pprint import pprint
from time import sleep
import urllib3
import re


# crawling용
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from decouple import config

# django db 저장용
import json
import os
import django


# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieback.settings")
django.setup()
from movies.models import *


movies = Movie.objects.all()
for movie in movies:
    title = movie.title
    base_url = f'https://search.daum.net/search?q={title}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #
    first_url = soup.select_one('#nmovie_img_0 .thumb')['href']
    movieId = first_url[43:]
    first_url = f'https://movie.daum.net/moviedb/main?movieId={movieId}'
    # https://movie.daum.net/data/movie/photo/movie/list.json?id=93004&pageNo=1&pageSize=10&adultFlag=F
    print(first_url)
    response = requests.get(first_url)
    print(response)
    # bs으로는 불가능
    # 1. 셀레니움 2. 
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)

    break
