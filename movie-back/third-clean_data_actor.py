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
    actors = movie.actors.all()
    for actor in actors:
        if actor.img_url == '':
            actorname = actor.name
            # href="./detail.nhn?code=136873"
            base_url = f'https://movie.naver.com/movie/bi/mi/detail.nhn?code={link[51:]}'
            print(link[51:])
            response = requests.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            print(actorname)
            try:
                print(soup.select_one(f'img[alt="{actorname}"]')['src'])
                photo = soup.select_one(f'img[alt="{actorname}"]')['src']    
                actor.img_url = photo
                print(actor.img_url)
                print(photo)
                print(actor)
                actor.save()
            except:
                actor.img_url = 'https://ssl.pstatic.net/static/movie/2012/06/dft_img120x150.png'
                print(actor.img_url)
                actor.save()