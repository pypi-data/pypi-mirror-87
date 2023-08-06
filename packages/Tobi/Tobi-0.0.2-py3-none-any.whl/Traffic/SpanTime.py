from urllib.parse import quote_plus, unquote
import xmltodict, json
import requests
from urllib.parse import urlencode


def spanTime(Near_Station_Lat, Near_Station_Lon):
    url = 'http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoBySubway'
    params = '?' + urlencode({
        quote_plus(
            "serviceKey"): "p%2FjvMYI4C7znYs1z7bwkpbC5XOPhQ2c5XMyRYcH6A%2BLnvRkIO95%2F9tyKecxg06ais5rGNSxsY6eplXsP3%2F%2FiSw%3D%3D",
        quote_plus("startX"): Near_Station_Lat,  # 좌표126.74
        quote_plus("startY"): Near_Station_Lon,  # 37.351828
        quote_plus("endX"): '126.74',  # 정왕역 좌표127.027637
        quote_plus("endY"): '37.351828',  # 37.497950
    })
    if (Near_Station_Lat == 126.742989 and Near_Station_Lon==37.351735):
        return "0"

    else:
        url = url + unquote(params)
        req = requests.get(url)
        xpars = xmltodict.parse(req.text)
        dump = json.dumps(xpars)
        data1 = json.loads(dump)
        # pd.DataFrame(data1['ServiceResult']['msgBody']['itemList']['pathList'])
        time = data1['ServiceResult']['msgBody']['itemList']['time']
        return str(time)
