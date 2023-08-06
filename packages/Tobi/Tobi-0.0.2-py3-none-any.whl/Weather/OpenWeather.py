import json, requests
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import pandas as pd
from PIL import Image
import numpy as np

# 좌표를 입력받고 정보를 다 출력해주는 함수 / 매개값 : '37.56826','126.977829' / 리턴값 : (11.13, 12.0, 10.0, nan, nan, nan, 1.49) / 다른 .py에서의 사용 x
def openWeather(lat, lon):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = '?' + urlencode({
        quote_plus("lat"): lat,                                # 도시
        quote_plus("lon"): lon,
        quote_plus("cnt"): '10',
        quote_plus("appid"): '98399fd9226e82728bde87664fa16b59',  # 인증키
        quote_plus("mode"): 'json',                               # 반환타입
        quote_plus("units"): 'metric'                             # 섭씨온도로 자동 변환
    })

    url = url+unquote(params)
    req = requests.get(url).content                  # url로 데이터 추출함 - 바이트타입 추출
    data1 = json.loads(req)
    weatherinfo = data1['weather'][0]
    wind = data1['wind']

    # 데이터 처리
    data = pd.DataFrame([data1['main']])
    data = data.transpose()
    data.columns = ['value']
    data = data['value'].to_dict()

    return (data['temp'], data['temp_max'], data['temp_min'], np.nan, np.nan, np.nan, wind['speed'])

if __name__ == "__main__":
    output = openWeather('37.56826','126.977829')
    print(output)