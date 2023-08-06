import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests, json
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
# 아래 3개의 함수는 KorWeather1에서 가져와서 썼음
from Weather.KorWeather import timeInfo, mapToGrid, getData


# 강수확률이랑 시간별 강수확률을 반환해주는 함수 / 매개값 : data(json), 시간표상 하교시간 or 집 도착시간 둘 중에 결정
# 리턴값 : 등교~하교 사이의 강수확률과 강수량을 평균값으로 반환, 각 시간별 강수확률 반환 -> 22일 저녁에 강수량도 같이 넣을 예정!!!!!!!!!!!!!!!
def rainPersentage(data, end_time):
    pd.set_option('mode.chained_assignment', None)  # SettingWithCopyWarning 경고 끄는 코드
    #     print(data)
    df = data[['category', 'fcstTime', 'fcstValue']]
    #          6시간 강수량, 온도, 강수확률
    save_category = ['R06', 'T3H', 'POP']
    save_index = [i for i, ch in enumerate(df['category']) for j in save_category
                  if ch == j]
    data = df.iloc[save_index]
    data.index = range(len(data))  # 인덱스 재정의

    for i in range(len(data)):
        data.iloc[i, 1] = data.iloc[i, 1][0:2]  # 1800 -> 18로 뒤에 00때는 코드
    #     print(data2.iloc[i, 1])

    # print(dict1, '\n', data2, '\n')
    POP = data.loc[data.category == 'POP']  # 강수확률
    R06 = data.loc[data.category == 'R06']  # 6시간 강수량
    T3H = data.loc[data.category == 'T3H']  # 3시간 기온

    #     print("강수확률")
    #     print(POP)

    try:
        POP['fcstTime'] = POP['fcstTime'].astype('int')
    except:
        pass

    POP.index = np.arange(len(POP))
    R06.index = np.arange(len(R06))
    T3H.index = np.arange(len(T3H))
    strat_time = 10  # 등교시간
    end_time = 22

    sum_per = 0.0
    sum_amount = R06['fcstValue'][0]
    index = 0.0
    dict1 = {}
    for i in range(len(POP)):
        if POP['fcstTime'][i] == 0:
            POP['fcstTime'][i] = 24
        if POP['fcstTime'][i] >= end_time:
            break
                # print(POP['fcstTime'][i], POP['fcstValue'][i])
        dict1[POP['fcstTime'][i]] = POP['fcstValue'][i]
        sum_per += float(POP['fcstValue'][i])  # 비 올 확률
        index = i + 1
    try:
        return (sum_per / index, sum_amount, dict1)
    except ZeroDivisionError:
        return ("ZeroDivisionError : POP['fcstTime'][i] >= end_time를 만족하는 인덱스값이 없습니다.", "", dict1)


# rainpersentage로부터 데이터를 받아와서 그래프를 그리기위한 함수
def rainData():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'
    data1 = getData(url, '37.518393', '126.737572')  # 집 위치 37.518393', '126.737572
    data2 = getData(url, '37.339873', '126.733557')  # 산기대 위치 37.339873, 126.733557
    rain_home = rainPersentage(data1, 22)  # 22 = 하교후 집 도착시간
    rain_school = rainPersentage(data2, 20)  # 20 = 하교시간

    if str(type(rain_home[0])) == "<class 'float'>":
        print("(집 기준)등교~하교시 비올 확률 : %0.1f, 예상 강수량 : %s" % (rain_home[0], rain_home[1]))
        print(rain_home[2], '\n')
        print("(학교 기준)등교~하교시 비올 확률 : %0.1f, 예상 강수량 : %s" % (rain_school[0], rain_school[1]))
        print(rain_school[2], '\n')

        # 그래프를 출력하는 코드 rain_home[2] == 시간별 강수 데이터(딕셔너리형)
        plt.plot(list(rain_home[2].keys()), list(rain_home[2].values()), 'go-', label="Home")
        plt.plot(list(rain_school[2].keys()), list(rain_school[2].values()), 'rs-', marker='*', label="KPU")
        plt.xlabel("time")
        plt.ylabel("value")
        plt.title("weather_info")
        plt.legend(loc=1)
        plt.axis([8, 22, 0, 3])
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.show()
        plt.savefig("1")

if __name__ == "__main__":
    rainData()