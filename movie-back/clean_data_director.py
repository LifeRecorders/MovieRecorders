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
    link = movie.naver_link
    directors = movie.directors.all()
    for director in directors:
        directorname = director.name
        # href="./detail.nhn?code=136873"
        base_url = f'https://movie.naver.com/movie/bi/mi/detail.nhn?code={link[51:]}'
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            if director.img_url == '':
                photo = soup.select_one(f'img[alt="{directorname}"]')['src']    
                director.img_url = photo
                print(director.img_url)
                print(photo)
                print(director)
                director.save()
        except:
            continue