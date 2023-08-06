import Weather.NaverWeather as na
import Weather.KorWeather as ka
import Weather.OpenWeather as oa
import pandas as pd
import numpy as np
import datetime, pytz, schedule, time

def weatherZip():
    pd.set_option('mode.chained_assignment', None)  # SettingWithCopyWarning 경고 끄는 코드
    home_lat = '37.518393'
    home_lon = '126.737572'
    lat = "37.3398"
    lon = "126.7335"
    nadata = na.naverWeather(lat, lon)
    kodata = ka.korWeather(home_lat, home_lon, lat, lon)
    ondata = oa.openWeather(lat, lon)
    now_time=str()

    try:
        kodata_backup = kodata[-2:]
        kodata = kodata[:-2]
        now_time = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%m월%d일 %H시%M분%S초')
        data = pd.DataFrame([nadata, kodata, ondata], columns=['현재온도', '최고온도', '최저온도', '비올확률', '강수량', '습도', '풍속'], index=['네이버 날씨', '기상청 날씨', '오픈 웨더 날씨'])
        weight = [15, 3, 2]  # 가중치 설정

        # 가중치 만큼 복사시키는 코드
        for i in np.arange(weight[0]):
            data.loc[i] = data.loc['네이버 날씨']  # data.index[0]

        for i in (np.arange(weight[1]) + weight[0]):
            data.loc[i] = data.loc['기상청 날씨']  # data.index[1]

        for i in (np.arange(weight[2]) + weight[0] + weight[1]):
            data.loc[i] = data.loc['오픈 웨더 날씨']  # data.index[2]

        print(data.head(3), "\n");

        data = data.astype('float')
        info = pd.DataFrame(data.mean(axis = 0), columns = ['가중치 적용한 평균값'])
        pd.options.display.float_format = '{:.1f}'.format  # 소수점 1자리만 나타내주는 코드
        info = info.transpose()
        info['time'] = [ka.timeInfo()]
        info['now_time'] = now_time
        # print(kodata)
        # print(kodata_backup)
        info['home_rain_per'] = kodata_backup[-2][0]
        info['home_rain_amount'] = kodata_backup[-2][1]
        info['school_rain_per'] = kodata_backup[-1][0]
        info['school_rain_amount'] = kodata_backup[-1][1]
        # pd.set_option('display.max_columns', 10)   # n개의 컬럼을 다 보여줘라~
        print(info[['현재온도', '비올확률', '강수량', 'now_time']])

        # 최초 실행시
        # dt = info.to_excel("test.xlsx", encoding='euc-kr')
        # 2번째 실행시
        dt = pd.read_excel("test.xlsx")
        dt = pd.concat([dt, data.head(3)], ignore_index=True)
        dt = pd.concat([dt, info], ignore_index=True)
        dt.to_excel("test.xlsx", encoding='euc-kr', index=False)
        print("test.xlsx에 저장 완료")
        print("------------------------------------------------------------------------")
        return

    except IOError:
        f = open("test_error.txt", "a")
        print("kodata : ", kodata)
        print("IOError에러발생 : test.xlsx파일이 열려있다면 닫아주세요\n" + now_time)
        f.write("IOError에러발생 : test.xlsx파일이 열려있다면 닫아주세요\n" + now_time)
        return


    except ValueError:
        print("kodata : ", kodata)
        f = open("test_error.txt", "a")
        print("ValueError에러발생 : " + now_time + '\n' + str(ka.timeInfo()) + '\n' + "ka.main2(home_lat, home_lon, lat, lon) 리턴값 : 오류가났습니다", kodata, '\n')
        f.write("ValueError에러발생 : " + now_time + '\n' + str(ka.timeInfo()) + '\n' + "ka.main2(home_lat, home_lon, lat, lon) 리턴값 : 오류가났습니다\n", kodata, '\n')
        return

    except ValueError:
        print("kodata : ", kodata)
        f = open("test_error.txt", "a")
        print("ValueError : could not convert string to float: '오'" + now_time + '\n' + str("ValueError : could not convert string to float: '오'" + '\n' + "ka.main2(home_lat, home_lon, lat, lon) 리턴값 : 오류가났습니다", kodata, '\n'))
        f.write("ValueError에러발생 : " + now_time + '\n' + str(ka.timeInfo()) + '\n' + "ka.main2(home_lat, home_lon, lat, lon) ValueError : could not convert string to float: '오'\n", kodata, '\n')
        return

        print()
    except:  # 예외 발생 확인을 위해 주석처리해둠
        print("kodata : ", kodata)
        f = open("test_error.txt", "a")
        print("에러발생 : " + now_time +'\n' + str(ka.timeInfo()) + '\n'  + kodata + '\n')
        f.write("에러발생 : " + now_time +'\n' + str(ka.timeInfo()) + '\n' + kodata + '\n')
        return

if __name__ == "__main__":
    weatherZip()
    schedule.every(1).minutes.do(weatherZip)
    # # schedule.every(10).seconds.do(weatherZip)
    while True:
        schedule.run_pending()
    #     # time.sleep(10)
