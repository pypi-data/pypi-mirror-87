import time
from Traffic import NearStation,ShuttleDict,ShuttleTimeGo,SpanTime,SpanTimeNaver,SubDict,SubTime
from Util import *
# dict_go.py 있어야함 -> 딕셔너리의 키는 시간, 값은 셔틀 분 데이터 값

start = time.time()

station_name = "갈산"
year = "2020"
month = "12"
day = "02"

dictgo = ShuttleDict.timetableGo
now_location = ['37.491575', '127.030912']
# now_location = Now_LatNLon()
nearsub1 = NearStation.nearSubStation(now_location[0], now_location[1])  # 좌표(현재 위치) -> 정왕역 (좌표로 부터 가까운 역 검색)
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks))

index1 = nearsub1.rstrip('역')  # 정왕역 -> 정왕
# n = time.localtime().tm_wday
n = 1
weeks = ['월', '화', '수', '목', '금']
# print(weeks[n])
# data = int(Eclass.eclass.eclass("2015162013", 'mouse3178!')[weeks[n]])
data = Eclass.eclass("2019152015", 'hoho1023!')[1][weeks[n]]
h1 = int(data['hour'])
m1 = int(data['minute'])
rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks))
temp = rjfflstlrks

std = ShuttleTimeGo.shuttleTimeGo(h1, m1, dictgo)
h2 = int(std[0])
m2 = int(std[1])

rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks-temp))
temp = rjfflstlrks

listu = SpanTimeNaver.returnListu(station_name, year, month, day, h2, m2)
for i in range(3):

    dict1 = {}
    dict1['starty'], dict1['startx'] = SubDict.subDict[index1]  # 정왕 -> 정왕역 좌표 [37.351735, 126.742989] (역이름으로 좌표 반환)
    time_info = listu[i][4]
    h3, m3 = listu[i][0], listu[i][1]

    rjfflstlrks = time.time() - start
    print('응답시간 = '+str(rjfflstlrks-temp))
    temp = rjfflstlrks

    Travel_time_bus = NearStation.nearBusStation(now_location[0], now_location[1])
    h4, m4 = SubTime.subTime(h3, m3, Travel_time_bus)

    rjfflstlrks = time.time() - start
    print('응답시간 = '+str(rjfflstlrks-temp))
    temp = rjfflstlrks

    h5, m5 = SubTime.subTime(h4, m4, 10)

    print("출발 시스템"+"-"*60)
    print("현재 위치에서 가장 가까운 역은 " + station_name + "역입니다.\n")
    print("출발 추천시간 (집-> 버스정류장) : " + str(h5) + "시 " + str(m5) + "분(예상소요시간 : 10분)\n")

    if Travel_time_bus > 4:
        print("버스정류장->%s역 : %s시 %s분(예상소요시간 : %s분)" % (station_name, str(h4), str(m4), str(Travel_time_bus)))

    print(station_name + "역 에서 출발해야하는 시간 : " + str(h3) + "시 " + str(m3) + "분(예상소요시간 : " + time_info + "분)")
    print("정왕역에서 출발하는 " + str(h2) + "시 " + str(m2) + "분 셔틀 탑승")
    print("학교에 도착해야하는 시간 : %d시 %d분 (시간표 정보 읽어오기)\n" % (h1, m1))

rjfflstlrks = time.time() - start
print('응답시간 = '+str(rjfflstlrks))