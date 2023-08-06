import requests, datetime, pytz, json

# visual-crossing-weather api사용 비올확률 데이터가 2가지 밖에 없어서 1가지더 추가하기 위해 11월 22일 개발중 데이터는 다 뽑았고 weatherzip에서 가중치 두고 결과 봐야함
def visualCrossing(lat, lon):
    url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
    time = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
    location = lat + "," + lon
    # location = "38.2651,126.4852"
    querystring = {"startDateTime" : time,
                    "location" : location,
                   "aggregateHours":"24",
                   "contentType":"json",
                   "shortColumnNames":"1",
                   "unitGroup":"uk"}

    headers = {
        'x-rapidapi-key': "64116e543bmshff42d2dff0a85abp1a1265jsn7ff77ead4b84",
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
    }
    print(url)
    response = requests.request("GET", url, headers=headers, params=querystring)

    text = response.text
    data = json.loads(text)
    return data['locations'][location]['values'][0]['pop']

print(visualCrossing("37.7398", "126.7335"))