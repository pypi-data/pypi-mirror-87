import json, requests
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from io import BytesIO
import numpy as np

# 날씨 이미지를 now_weather.png 파일로 저장시켜주는 코드 / 매개값 : x / 리턴값 : x -> 이미지파일로 저장(출력)
def imgFile():
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = '?' + urlencode({
        quote_plus("lat"): "34.568",                                # 도시
        quote_plus("lon"): "126.977",
        quote_plus("cnt"): '5',
        quote_plus("appid"): '98399fd9226e82728bde87664fa16b59',  # 인증키
        quote_plus("mode"): 'json',                               # 반환타입
        quote_plus("units"): 'metric'                             # 섭씨온도로 자동 변환
    })

    url = url+unquote(params)
    req = requests.get(url).content                  # url로 데이터 추출함 - 바이트타입 추출
    data1 = json.loads(req)
    weatherinfo = data1['weather'][0]

    #     현재 기상정보 사진 가져와주는 코드 이후에 개발완료
    imgurl = 'http://openweathermap.org/img/wn/' + weatherinfo['icon'] + '@2x.png'
    req = requests.get(imgurl).content
    img = Image.open(BytesIO(req))
    img_matrix = np.array(img)
    plt.imshow(img_matrix)
    img.save('now_weather.png')
