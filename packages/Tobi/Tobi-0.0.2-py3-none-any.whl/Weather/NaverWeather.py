from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from urllib.parse import quote, urlencode, quote_plus, unquote
import urllib, re, json
from Util.Gpss import reverseLocation

# 좌표값으로 웹크롤링한 데이터를 반환해준다. / 매개값 : ("37.3398", "126.7335") / 리턴값 : 좌표와 날씨의 키워드로 검색한 모든 데이터 / 다른 .py파일에서의 사용 x
def getData(lat, lon):
    location = reverseLocation(lat, lon)  # resurn : 경기도 시흥시 정왕1동
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + quote(location + '날씨')
    # print(url)
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup_text = bs(html, 'html5lib')
    # print(soup_text)
    return soup_text

# 2. 기상정보 출력, 3. 강수유무 출력 / 매개값 : ("37.3398", "126.7335") / 리턴값 : ('1', '6', '2', '30', 0.0, '75', '1') / 다른 .py파일에서의 사용 x
def naverWeather(lat, lon):
    s = getData(lat, lon)

    # 맑음, 어제보다 1도 낮아요 - 모니터 인터페이스로 구성
    t2 = s.find('ul', class_='info_list').find('p', class_='cast_txt').text
    # 비올 확률 (미래)  .find_all('dd', class_='weather_item _dotWrapper') - 개발중
    # rain_hour = str(s.find_all('li', class_= 'on merge1'))
    # print(type(rain_hour))

    # 현재 기온
    tnow = s.find('p', class_='info_temperature').find('span', class_='todaytemp').text  # + '℃'
    # 최고 기온
    tmax = s.find('span', class_='merge').find('span', class_='max').find('span', class_='num').text  # + '℃'
    # 최저 기온
    tmin = s.find('span', class_='merge').find('span', class_='min').find('span', class_='num').text  # + '℃'
    # 현재 비올 확률
    rain = s.find('li', class_='on now merge1').find('dd', class_='weather_item _dotWrapper').text
    # 현재 강수량
    rain_data = s.find('li', class_='on now merge1').find('dd', class_='item_condition').text.strip()
    rain_amount = (float(rain_data[0])+float(rain_data[-1]))/2
    # 현재 습도
    reh = s.find('div', class_='info_list humidity _tabContent _center').find('dd', class_='weather_item _dotWrapper').find('span').text
    # 현재 풍속
    wind = s.find('div', class_='info_list wind _tabContent _center').find('dd', class_='weather_item _dotWrapper').find('span').text  # + 'm/s'

    #   현재온도, 최고온도, 최저온도, 비올확률,       강수량,   습도, 풍속
    return (tnow, tmax, tmin, rain.strip().replace('%', ''), rain_amount, reh, wind)

# 경지가 개발한 좌표를 주소로 바꿔주는 코드 / 매개값 : "37.340037", "126.733381" / 리턴값 : 경기도 시흥시 정왕1동 / 아마 다른 파일에서도 사용할 듯

if __name__ == "__main__":
    print(naverWeather("37.3398", "126.7335"))  # 학교 온도 개발 완료