import hashlib
import hmac
import base64
import requests
import time
import numpy as np
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, unquote
import json
from urllib.request import urlopen, Request
import urllib
import bs4

def ipCall():
    enc_location = urllib.parse.quote("ip 주소 확인")
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'html5lib')
    ip=soup.select("div[class=ip_chk_box]")
    name = str(ip[0])
    answer = name[24:]
    array = answer.split("<")
    return array[0]

# Signature Make
def makeSignature(method, basestring, timestamp, access_key, secret_key):
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'utf-8')
    signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return signature

def requestApi(timestamp, access_key, signature, uri):
    # Header for Request
    headers = {'x-ncp-apigw-timestamp': timestamp,
               'x-ncp-iam-access-key': access_key,
               'x-ncp-apigw-signature-v2': signature}

    # Geolocation API Request
    res = requests.get(uri, headers=headers)

    # Check Response
    content = res.content.decode(encoding='utf-8')
    content1 = content.split(",")
    content1=np.array(content1)
    content1[7]=content1[7].replace('"lat": ','')
    content1[8]=content1[8].replace('"long": ','')
    return content1[7],content1[8]

def reverseLocation(lat,lon):     #파라미터로 위도 경도 와야함(위도 경도로 위치정보 구하는 api)
    lat = lat  # 한국산업기술대학교 위도("37.340037")
    lon = lon  # 한국산업기술대학교 경도("126.733381")
    key = "l7xx00cd3e8e95cc4fee84f48861b2d6d812"  # api 키

    url = "https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1"
    queryParams = "&" + urlencode({quote_plus('lat'): lat,
                                   quote_plus('lon'): lon,
                                   quote_plus('coordType'): "WGS84GEO",
                                   quote_plus('addressType'): "A01",
                                   quote_plus('appKey'): key})

    request = urllib.request.Request(url + unquote(queryParams))
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    decode = response_body.decode('utf-8')
    json_data = json.loads(decode)
    return(json_data["addressInfo"]["fullAddress"])  # json을 조작하여 위도경도 다시 반환가능

def location():
    # Signature 생성에 필요한 항목
    method = "GET"
    ipname = ipCall()
    basestring = "/geolocation/v2/geoLocation?ip="+ipname+"&ext=t&responseFormatType=json"
    timestamp = str(int(time.time() * 1000))
    access_key = "1bl8GtXyTTzXDCG4lgrA"  # access key id (from portal or sub account)
    secret_key = "C43S00RfBboTCIm89TlO8DxqLzChvuLBgr0fO2SD"  # secret key (from portal or sub account)
    secret_key = bytes(secret_key, 'UTF-8')
    signature = makeSignature(method, basestring, timestamp, access_key, secret_key)

    # GET Request
    hostname = "https://geolocation.apigw.ntruss.com"
    requestUri = hostname + basestring
    (lat, lon) = requestApi(timestamp, access_key, signature, requestUri)

    return (lat, lon)

if __name__ == "__main__":
    print(location())
    print(reverseLocation(location()[0],location()[1]))