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

movieCdlist = []
movieNamelist = []
movieDicts = {}
def jinheungAPI():
    global movieDicts, movieCdlist, movieNamelist
    # 현재부터 과거까지의 원하는 주간을 입력
    key = 'd1de3e876f25122ef07b40f0a7d982e4'

    def week(week_number): # 원하는 만큼의 주간을 입력
        week_list = []
        for week in range(1, week_number+1):
            targetDt = datetime(2018, 11, 28) - timedelta(weeks=week) 
            targetDt = targetDt.strftime('%Y%m%d') # yyymmdd
            week_list.append(targetDt)
        return week_list
    
    sleep(0.05)
    api_url_list = []
    for targetDt in week(50): ### data parsing 조절
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
        # 우리가 원하는 multiMovieYn, repNationCd, wideAreaCd는 이미 default값이므로 따로 지정하지 않습니다.
        api_url = f'{base_url}?key={key}&targetDt={targetDt}'
        api_url_list.append(api_url)

    for api_url in api_url_list:
        response = requests.get(api_url) # 200
        data = response.json()
        # 데이터를 잘 가져왔는지 확인 합니다.
        # 여기서 나오는 값들을 models.py의 db에 저장
        try:
            weeklyBoxOfficeLists = data.get('boxOfficeResult').get('weeklyBoxOfficeList')
        except AttributeError:
            continue

        # 여기 dict를 활용해서 바로 저장
        for weeklyBoxOfficeList in weeklyBoxOfficeLists:
            movieCd = weeklyBoxOfficeList.get('movieCd')
            ##
            if Movie.objects.filter(movieCd=movieCd).exists() == False:
                movie = Movie()
                movie.movieCd = movieCd
                movieNm = weeklyBoxOfficeList.get('movieNm') 
                movie.title = movieNm

                audiCnt = weeklyBoxOfficeList.get('audiCnt')
                movie.audience = audiCnt

                openDt = weeklyBoxOfficeList.get('openDt')
                movie.open_date = openDt

                rank = weeklyBoxOfficeList.get('rank')
                movie.rank = rank
                movie.save()

                movieNamelist.append(movieNm)

                if movieDicts.get(movieCd) == None:
                    movieCdlist.append(movieCd)
                    movieDicts[movieCd] = {
                        'movieCd':movieCd,
                        'movieNm':movieNm,
                        'audiCnt':audiCnt,
                        'openDt':openDt,
                        'rank':rank
                        }
                print('-1', movieCd)

            else:
                print('이미 존재하는 movieCd')
                # movie = Movie.objects.get(movieCd=movieCd)
            
    # 여기서 받은 영화이름 정보를 가지고 영화목록 API에서 감독 등등 정보 가지고 올것
    # pprint('1 ----------------------')
    # pprint(movieDicts)

    sleep(0.05)
    # api_url_list = []
    for movieCd in movieCdlist:
        print('-2', movieCd)
        movie = Movie.objects.get(movieCd=movieCd)
        movieNm = movieDicts[movieCd]['movieNm']
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
        api_url = f'{base_url}?key={key}&movieNm={movieNm}'
        # 필요없어
        # api_url_list.append(api_url)

        # for api_url in api_url_list:
        response = requests.get(api_url) # 200
        data = response.json()
        # pprint(data)

        movieList = data.get('movieListResult').get('movieList')[0]
        print(movieList)

        # movieDicts[movieCd]['director'] = []
        # movieDicts[movieCd]['companyNm'] = []
        # for movieList in movieLists:
        companys = movieList.get('companys')
        for company in companys:
            # print(company)
            companyname = company.get('companyNm')
            movie.company = companyname
            movieDicts[movieCd]['companyNm'] = companyname
            break

        movieNmEn = movieList.get('movieNmEn')
        genreAlt = movieList.get('genreAlt')
        nationAlt = movieList.get('nationAlt')
        movieDicts[movieCd]['movieNmEn'] = movieNmEn
        movie.title_en = movieNmEn
        ## -----------------------------------------ManyToManyField
        if genreAlt != '':
            if ',' in genreAlt:
                genres_cleans = genreAlt.split(',')
                for genre_clean in genres_cleans:
                    if Genre.objects.filter(genreType=genre_clean).exists() == False:
                        genretype = Genre()
                        genretype.genreType = genre_clean
                        genretype.save()
                        movie.genres.add(genretype)
                    elif Genre.objects.filter(genreType=genre_clean).exists() == True:
                        genretype = Genre.objects.filter(genreType=genre_clean).first()
                        movie.genres.add(genretype)
            else:
                if Genre.objects.filter(genreType=genreAlt).exists() == False:
                    genretype = Genre()
                    genretype.genreType = genreAlt
                    genretype.save()
                    movie.genres.add(genretype)
                elif Genre.objects.filter(genreType=genreAlt).exists() == True:
                    genretype = Genre.objects.filter(genreType=genreAlt).first()
                    movie.genres.add(genretype)
                else:
                    continue

        movieDicts[movieCd]['genreAlt'] = genreAlt.split(',')
        movieDicts[movieCd]['nationAlt'] = nationAlt
        movie.nation = nationAlt
        movie.save()

    sleep(0.05)

    # movies = Movie.objects.all()
    # print(movies.movieCd)
    # print(movies)
    # for movieCd in movies:
    #     movieCd = movieCd['movieCd']
    

    for movieCd in movieCdlist:
        print('-3', movieCd)
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        api_url = f'{base_url}?key={key}&movieCd={movieCd}'
        # api_url_list.append(api_url)
        # for api_url in api_url_list:
        movie = Movie.objects.get(movieCd=movieCd)
        response = requests.get(api_url) # 200
        data = response.json()
        movieLists = data.get('movieInfoResult').get('movieInfo')
        showTm = movieLists.get('showTm')
        movie.running_time = showTm

        # 영화정보 하나가 들어온다. 그래서 벗겨낼 것 없이 접근함
        movieDicts[movieCd]['link'] = ''
        movieDicts[movieCd]['actorinfo'] = []
        movieDicts[movieCd]['directorinfo'] = []
        movieDicts[movieCd]['watchGradeNm'] = []
        # {'cast': '모티시아','castEn': 'Morticia Addams','peopleNm': '샤를리즈 테론','peopleNmEn': 'Charlize Theron'},                          
        # 리스트로 저장

        actors = movieLists.get('actors')
        movieDicts[movieCd]['actorinfo'] = actors
        print('---------------')
        for actor in actors:
            peopleNm = actor['peopleNm']
            peopleNmEn = actor['peopleNmEn']
            cast = actor['cast']
            castEn = actor['castEn']
            # ---------------------------ManyToManyField
            if Actor.objects.filter(name=peopleNm).exists() == False:
                actorinstance = Actor()
                actorinstance.name = peopleNm
                actorinstance.name_en = peopleNmEn
                actorinstance.save()
                castinstance = Cast.objects.create(movie=movie, actor=actorinstance)
                castinstance.cast = cast
                castinstance.cast_en = castEn
                castinstance.save()
                # movie.actor.add(actorinstance)
            else:
                # 여기 다시 확인
                actorinstance = Actor.objects.filter(name=peopleNm).first()
                castinstance = Cast.objects.create(movie=movie, actor=actorinstance)
                castinstance.cast = cast
                castinstance.cast_en = castEn
                castinstance.save()
                # movie.actor.add(actorinstance)

        try:
            watchGradeNm = movieLists.get('audits')[0].get('watchGradeNm')
            pprint(watchGradeNm)
            movieDicts[movieCd]['watchGradeNm'] = watchGradeNm
            movie.watch_grade = watchGradeNm    
        except IndexError:
            movieDicts[movieCd]['watchGradeNm'] = '15세이상관람가'
            movie.watch_grade = '15세이상관람가'
        # ---------------------------ManyToManyField
        # directors {'peopleNm': '그렉 티어넌', 'peopleNmEn': 'Greg Tiernan'},
        directors = movieLists.get('directors')
        movieDicts[movieCd]['directorinfo'] = directors
        for director in directors:
            peopleNm = director['peopleNm']
            peopleNmEn = director['peopleNmEn']
            # ---------------------------ManyToManyField
            if Director.objects.filter(name=peopleNm).exists() == False:
                directorinstance = Director()
                directorinstance.name = peopleNm
                directorinstance.name_en = peopleNmEn
                directorinstance.save()
                movie.directors.add(directorinstance)
            elif Director.objects.filter(name=peopleNm).exists() == True:
                # 여기 다시 확인
                directorinstance = Director.objects.filter(name=peopleNm).first()
                movie.directors.add(directorinstance)
        movie.save()

    return 


def NaverAPI():
    # 활용해서 찾아오기
    global movieDicts, movieCdlist, movieNamelist
    print('naver 크롤링이 시작됩니다.')
    Client_ID = 'qFWW89KMUR5Yi8sM0B7E'
    Client_Secret = '8PcSTDLJLU'

    for movieCd in movieCdlist:
        print('--naver4', movieCd)
        movie = Movie.objects.get(movieCd=movieCd)
        query = movieDicts[movieCd]['movieNm']
        openDt = movieDicts[movieCd]['openDt']
        openDt = openDt[:4]
        BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
        HEADERS = {
            'X-Naver-Client-Id' : Client_ID,
            'X-Naver-Client-Secret' : Client_Secret, #trailing convention
        }

        API_URL = f'{BASE_URL}?query={query}'
        response = requests.get(API_URL, headers=HEADERS).json()
        items = response.get('items')
        print('error 잡자!!!!!!!!')
        pprint(items)

        if len(items):
            item = items[0]
        else:
            continue

        movieDicts[movieCd]['link'] = ''
        if item['link']:
            movieDicts[movieCd]['link'] = item['link']
            movie.naver_link = item['link']
        movieDicts[movieCd]['userRating'] = item['userRating']
        userRating = item['userRating']
        movie.rating = userRating

        if item['pubDate'] == openDt: #pubDate 최신일자로 검증 'pubDate': '2018'
            if item['image'] != '': #영화 썸네일 이미지의 URL 이 없는 경우 저장하지 않습니다.
                if movieDicts.get(movieCd) != None:
                    movieDicts[movieCd]['image'] = item['image']

        movie.save()

    return


# def single_line(raw_str):
#     return " ".join(raw_str.split())

# def uni_to_utf8(unicode_str):
#     return str(unicode_str.encode('utf-8'))

# 감독, 연기자 사진
def NaverCrawling():
    global movieCdlist, movieDicts
    # movies = Movie.objects.values('movieCd')
    print('NaverCrawling 시작합니다.')
    pprint(movieDicts)
    for movieCd in movieCdlist:
        movie = Movie.objects.get(movieCd=movieCd)
        # movieCd = movieCd['movieCd']
        # print('--naver5', movieCd)
        # movie = Movie.objects.get(movieCd=movieCd)
        try:
            if movieDicts[movieCd]['link'] != '':
                base_url = movieDicts[movieCd]['link']
                response = requests.get(base_url)
                # print(response)
                soup = BeautifulSoup(response.content, 'html.parser')
                # print(soup)
                peoplelist = movieDicts[movieCd]['actorinfo']
                for idx in range(len(peoplelist)):
                    try:
                        peopleNm = peoplelist[idx]['peopleNm']
                        data = soup.select_one(f'img[alt="{peopleNm}"]')['src']

                        if Actor.objects.filter(name=peopleNm).exists() == True:
                            actorinstance = Actor.objects.filter(name=peopleNm).first()
                            actorinstance.img_url = data
                            actorinstance.save()
                            movie.actor.add(actorinstance)
                        movieDicts[movieCd]['actorinfo'][idx]['img_url'] = data
                    except:
                        movieDicts[movieCd]['actorinfo'][idx]['img_url'] = ''

                peoplelist = movieDicts[movieCd]['directorinfo']
                for idx in range(len(peoplelist)):
                    try:
                        peopleNm = peoplelist[idx]['peopleNm']
                        data = soup.select_one(f'img[alt="{peopleNm}"]')['src']
                        if Director.objects.filter(name=peopleNm).exists() == True:
                            directorinstance = Director.objects.filter(name=peopleNm).first()
                            directorinstance.img_url = data
                            directorinstance.save()
                            movie.director.add(directorinstance)
                        movieDicts[movieCd]['directorinfo'][idx]['img_url'] = data
                    except:
                        movieDicts[movieCd]['directorinfo'][idx]['img_url'] = ''

                if movieDicts[movieCd]['genreAlt'] == [''] or movieDicts[movieCd]['genreAlt'] == '' or movieDicts[movieCd]['genreAlt'] == []:
                    data = soup.select("dl.info_txt1 dd:nth-of-type(1) a")
                    if data != []:
                        genretype = Genre()
                        genretype.genreType = data
                        genretype.save()
                        movie.genres.add(genretype)

                try:
                    poster_naver_url = soup.select_one("div.poster a img")['src']
                    movieDicts[movieCd]['poster_naver_url'] = poster_naver_url
                    movie.naver_poster_url = poster_naver_url
                    # pprint(poster_naver_url)
                    content = soup.find('div',class_='story_area')
                    raw_main_story = content.find('p',class_='con_tx').text

                    if not raw_main_story:
                        movieDicts[movieCd]['description'] = ''
                        return None
                except:
                    continue

 
                # raw_main_story = raw_main_story.prettify(formatter="html")
                # raw_main_story = (re.sub(r'<.*>',"",raw_main_story))
                # uni_main_story = single_line((re.sub(r'&.*;',"",raw_main_story)))
                # main_story = uni_to_utf8(uni_main_story)
                movieDicts[movieCd]['description'] = raw_main_story
                movie.description = raw_main_story
                movie.save()
        except KeyError:
            print('keyerror')
            print(movieDicts[movieCd])

# def collectionCrawling():
#     # https://www.kmdb.or.kr/db/list/detail/143/0902
#     # collection 별로 해당 영화이름을 따와서 저장
#     pass

# def KMDb():
#     # collection에서 따온 이름으로 찾아서 movieDicts 저장
#     # https://www.data.go.kr/dataset/3035985/openapi.do
#     # https://github.com/ud803/ud803.github.io/blob/c456ecf3cd1e1a465646be9e8c9889f8f9d041c9/_posts/2018-09-03-%EC%98%81%ED%99%94%EC%A7%84%ED%9D%A5%EC%9C%84%EC%9B%90%ED%9A%8C%20API%EB%A5%BC%20%ED%99%9C%EC%9A%A9%ED%95%9C%202017%EB%85%84%20%EA%B0%9C%EB%B4%89%20%EC%98%81%ED%99%94%20%EB%B6%84%EC%84%9D.md
#     pass


# 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__ == '__main__':
    # Movie.objects.all().delete()
    # Genre.objects.all().delete()
    # Director.objects.all().delete()
    # Actor.objects.all().delete()
    # Cast.objects.all().delete()

    jinheungAPI()
    # collectionCrawling()
    # KMDb()
    NaverAPI()
    NaverCrawling()
    # pprint(movieDicts)