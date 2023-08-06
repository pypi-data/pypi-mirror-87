from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, unquote
import json
from urllib.request import urlopen
import urllib


# 인자값 : 역 코드, 년, 달, 일, 시간, 분


def spanTimeNaver(dptcode, year, month, date, hour, minute):
    dict_station = {"갈산": "20117", "금정": "443", "기흥": "1537", "강남": "222"}
    dptcoded = dict_station[dptcode]
    url = "https://map.naver.com/v5/api/subway/search?"
    time = str(year) + '-' + str(month) + '-' + str(date) + 'T' + str(hour) + '%3A' + str(minute) + '%3A00'
    queryParams = "&" + urlencode({quote_plus('start'): str(dptcoded),
                                   quote_plus('goal'): "455",
                                   quote_plus('option%5B%5D'): "false%2Cfalse",
                                   quote_plus('serviceDay'): '1',
                                   quote_plus('arrivalTime'): time})

    request = urllib.request.Request(url + unquote(queryParams))
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    decode = response_body.decode('utf-8')

    try:
        json_data = json.loads(decode)
        datad = json_data['paths'][0]['departureTime']
        dataa = json_data['paths'][0]['alarmArrivalTime']
        return datad[-8:-6], datad[-5:-3], dataa[-8:-6], dataa[-5:-3]
    except:
        return "err"


def timeToTempTime(hour_m, minute_m):
    if len(str(minute_m)) == 1:
        temp_minute = "0" + str(minute_m)
    else:
        temp_minute = str(minute_m)
    if len(str(hour_m)) == 1:
        temp_hour = "0" + str(hour_m)
    else:
        temp_hour = str(hour_m)
    return temp_hour, temp_minute

def spanTimeMinute(h1,m1,h2,m2):
    if h1[0] == '0':
        h1i = int(h1[1])
    else:
        h1i = int(h1)
    if m1[0] == '0':
        m1i = int(m1[1])
    else:
        m1i = int(m1)
    if h2[0] == '0':
        h2i = int(h2[1])
    else:
        h2i = int(h2)
    if m2[0] == '0':
        m2i = int(m2[1])
    else:
        m2i = int(m2)
    cm1 = h1i*60 + m1i
    cm2 = h2i*60 + m2i
    return h1i, m1i, h2i, m2i, str(cm2 - cm1)



def returnListu(station_name, year, month, day, hour, minute):
    lis = []
    temp_time = timeToTempTime(hour, minute)
    data = spanTimeNaver(station_name, year, month, day, temp_time[0], temp_time[1])
    data = spanTimeMinute(data[0], data[1], data[2], data[3])
    lis.append(data)

    i = 0
    while len(lis) < 3:
        if minute < 0:
            minute = 59
            hour -= 1
        temp_time = timeToTempTime(hour, minute)
        data = spanTimeNaver(station_name, year, month, day, temp_time[0], temp_time[1])
        data = spanTimeMinute(data[0], data[1], data[2], data[3])
        if lis[i] == data:
            minute -= 1
            continue
        else:
            lis.append(data)
            i += 1
        minute -= 2
    return lis
# 상현

station_name = "갈산"
year = "2020"
month = "12"
day = "02"
hour = 9
minute = 15
listu = returnListu(station_name, year, month, day, hour, minute)
print(listu)

# 출발시간, 출발 분, 도착시간, 도착 분, 소요시간