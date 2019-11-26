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
from movies.models import Movie

movieCdlist = []
movieNamelist = []
movieDicts = {}
def jinheungAPI():
    global movieDicts, movieCdlist, movieNamelist
    # 현재부터 과거까지의 원하는 주간을 입력
    key = '333585f0b647de27e23b3d9ef596e413'

    def week(week_number): # 원하는 만큼의 주간을 입력
        week_list = []
        for week in range(1, week_number+1):
            targetDt = datetime(2019, 11, 25) - timedelta(weeks=week) 
            targetDt = targetDt.strftime('%Y%m%d') # yyymmdd
            # pprint(targetDt)
            week_list.append(targetDt)
        return week_list
    
    sleep(0.05)
    api_url_list = []
    for targetDt in week(1): ### data parsing 조절
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
        # 우리가 원하는 multiMovieYn, repNationCd, wideAreaCd는 이미 default값이므로 따로 지정하지 않습니다.
        api_url = f'{base_url}?key={key}&targetDt={targetDt}'
        api_url_list.append(api_url)

    for api_url in api_url_list:
        response = requests.get(api_url) # 200
        data = response.json()
        # pprint(data) # 데이터를 잘 가져왔는지 확인 합니다.
        # 여기서 나오는 값들을 models.py의 db에 저장

        weeklyBoxOfficeLists = data.get('boxOfficeResult').get('weeklyBoxOfficeList')
        #print(weeklyBoxOfficeList)

        # 여기 dict를 활용해서 바로 저장
        for weeklyBoxOfficeList in weeklyBoxOfficeLists:
            movieCd = weeklyBoxOfficeList.get('movieCd')
            movieNm = weeklyBoxOfficeList.get('movieNm') 
            audiCnt = weeklyBoxOfficeList.get('audiCnt')
            openDt = weeklyBoxOfficeList.get('openDt')
            rank = weeklyBoxOfficeList.get('rank')
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
    # 여기서 받은 영화이름 정보를 가지고 영화목록 API에서 감독 등등 정보 가지고 올것
    # pprint('1 ----------------------')
    # pprint(movieDicts)

    sleep(0.05)
    api_url_list = []
    for movieCd in movieCdlist:
        
        movieNm = movieDicts[movieCd]['movieNm']
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
        api_url = f'{base_url}?key={key}&movieNm={movieNm}'
        api_url_list.append(api_url)

        for api_url in api_url_list:
            response = requests.get(api_url) # 200
            data = response.json()
            # pprint(data)
            try:
                movieLists = data.get('movieListResult').get('movieList')
            except:
                continue

        # movieDicts[movieCd]['director'] = []
        movieDicts[movieCd]['companyNm'] = []
        for movieList in movieLists:
            # directors = movieList.get('directors')
            # for director in directors:
            #     director = director['peopleNm']
            #     movieDicts[movieCd]['director'].append(director)
            
            companys = movieList.get('companys')
            for company in companys:
                company = company['companyNm']
                movieDicts[movieCd]['companyNm'].append(company)
            movieNmEn = movieList.get('movieNmEn')
            genreAlt = movieList.get('genreAlt')
            nationAlt = movieList.get('nationAlt')
            movieDicts[movieCd]['movieNmEn'] = movieNmEn
            movieDicts[movieCd]['genreAlt'] = genreAlt.split(',')
            movieDicts[movieCd]['nationAlt'] = nationAlt

    # pprint('2 ----------------------')
    # pprint(movieDicts)
    # 무비상세

    sleep(0.05)
    api_url_list = []
    for movieCd in movieCdlist:
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        api_url = f'{base_url}?key={key}&movieCd={movieCd}'
        api_url_list.append(api_url)
        for api_url in api_url_list:
            response = requests.get(api_url) # 200
            data = response.json()
            # pprint(data)
            movieLists = data.get('movieInfoResult').get('movieInfo')
            # 영화정보 하나가 들어온다. 그래서 벗겨낼 것 없이 접근함
            movieDicts[movieCd]['actorinfo'] = []
            movieDicts[movieCd]['directorinfo'] = []
            movieDicts[movieCd]['watchGradeNm'] = []
            # {'cast': '모티시아','castEn': 'Morticia Addams','peopleNm': '샤를리즈 테론','peopleNmEn': 'Charlize Theron'},                          
            # 리스트로 저장
            try:
                actors = movieLists.get('actors')
                movieDicts[movieCd]['actorinfo'] = actors
            
                # audits {watchGradeNm} 
                watchGradeNm = movieLists.get('audits')[0].get('watchGradeNm')
                movieDicts[movieCd]['watchGradeNm'] = watchGradeNm    
                    
                # directors {'peopleNm': '그렉 티어넌', 'peopleNmEn': 'Greg Tiernan'},
                directors = movieLists.get('directors')
                movieDicts[movieCd]['directorinfo'] = directors
            except:
                continue

    return 


def NaverAPI():
    # 활용해서 찾아오기
    global movieDicts, movieCdlist, movieNamelist

    Client_ID = 'qFWW89KMUR5Yi8sM0B7E'
    Client_Secret = '8PcSTDLJLU'
    
    for movieCd in movieCdlist:
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
        
        try:
            for item in items:

                if item['pubDate'] == openDt: #pubDate 최신일자로 검증 'pubDate': '2018'
                    if item['image'] != '': #영화 썸네일 이미지의 URL 이 없는 경우 저장하지 않습니다.
                        if movieDicts.get(movieCd) != None:
                            movieDicts[movieCd]['link'] = item['link']
                            movieDicts[movieCd]['image'] = item['image']
                            movieDicts[movieCd]['userRating'] = item['userRating']

                else:
                    continue

        except TypeError:
            continue
    return


# def single_line(raw_str):
#     return " ".join(raw_str.split())

# def uni_to_utf8(unicode_str):
#     return str(unicode_str.encode('utf-8'))

# 감독, 연기자 사진
def NaverCrawling():
    global movieCdlist, movieDicts
    for movieCd in movieCdlist:
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
                # data = data['src']
                movieDicts[movieCd]['actorinfo'][idx]['img_url'] = data
            except:
                movieDicts[movieCd]['actorinfo'][idx]['img_url'] = ''

        peoplelist = movieDicts[movieCd]['directorinfo']
        for idx in range(len(peoplelist)):
            try:
                peopleNm = peoplelist[idx]['peopleNm']
                data = soup.select_one(f'img[alt="{peopleNm}"]')['src']
                # data = data['src']
                movieDicts[movieCd]['directorinfo'][idx]['img_url'] = data
            except:
                movieDicts[movieCd]['directorinfo'][idx]['img_url'] = ''

        if movieDicts[movieCd]['genreAlt'] == ['']:
            data = soup.select("dl.info_txt1 dd:nth-of-type(1) a")
            if not data:
                movieDicts[movieCd]['genreAlt'] = []
                return None 
            else:
                movieDicts[movieCd]['genreAlt'] = []
                movieDicts[movieCd]['genreAlt'].append(data)
        
        data = soup.select_one("div.poster a img")['src']
        movieDicts[movieCd]['poster_naver_url'] = data

        content = soup.find('div',class_='story_area')
        raw_main_story = content.find('p',class_='con_tx').text
        if not raw_main_story:
            movieDicts[movieCd]['description'] = ''
            return None
        # raw_main_story = raw_main_story.prettify(formatter="html")
        # raw_main_story = (re.sub(r'<.*>',"",raw_main_story))
        # uni_main_story = single_line((re.sub(r'&.*;',"",raw_main_story)))
        # main_story = uni_to_utf8(uni_main_story)
        movieDicts[movieCd]['description'] = raw_main_story


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
    jinheungAPI()
    # collectionCrawling()
    # KMDb()
    NaverAPI()
    NaverCrawling()
    pprint(movieDicts)

    # movie = Movie(dict)
    # movie.genres = 
    # movie.title = 
    # movie.title_en = 
    # movie.description = 
    # movie.open_date = 
    # movie.audience = 
    # movie.poster_url = 
    # movie.director = 
    # movie.actor = 
    # movie.cast = 
    # movie.watch_grade = 
    # movie.running_time = 
    # movie.nation =
    # movie.movieCd = 
    # movie.rank = 
    # movie.trailor_url = 
    # movie.save()


