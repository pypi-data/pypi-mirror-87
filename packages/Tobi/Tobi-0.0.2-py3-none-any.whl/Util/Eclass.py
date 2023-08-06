from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def eclass(id,password):

    #크롬창을 띄우지 않는 옵션
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    # 위치 지정
    driver = webdriver.Chrome("Chromedriver.exe", options=options)

    # 웹 자원 로드를 위해 암묵적으로 딜레이
    delay_time = 3
    driver.implicitly_wait(delay_time)

    # URL 접속 시도
    driver.get('http://eclass.kpu.ac.kr/ilos/main/member/login_form.acl')

    # ID, PW 입력
    # usr_id = input("ID를 입력해주세요 :")
    # usr_pwd = input("PW를 입력해주세요 :")
    usr_id = id
    usr_pwd = password
    driver.find_element_by_name('usr_id').send_keys(usr_id)
    driver.find_element_by_name('usr_pwd').send_keys(usr_pwd)

    # 로그인 버튼 클릭
    driver.find_element_by_xpath('//*[@id="myform"]/div/div/div/div').click()

    # URL 접속 시도
    driver.get("http://eclass.kpu.ac.kr/ilos/main/main_form.acl")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # notices = driver.find_element_by_class_name('title-01').text
    # print(notices)

    # notices = soup.select('div.p_inr > div.p_info > a > span')
    name1 = soup.select('div > ol > li > em')
    time1 = soup.select('div > ol > li > span')

    eclass = []
    for item in zip(name1, time1):
        eclass.append(
            {
                'name': item[0].text.replace('\n', '').strip(),
                'time': item[1].text.replace('\n', '').strip()
            }
        )

    data = pd.DataFrame(eclass)
    index = 0
    for i, ch in enumerate(data['name']):
        data['name'][i] = data['name'][i][:-42]

    tmp_index = []
    for i, ch in enumerate(data['time']):
        if len(ch) == 0:
            tmp_index.append(i)  # sdu index를 리스트로 저장

        elif ch[0] not in ['월', '화', '수', '목', '금']:
            #         print(index)
            index = i
            break

    for i in tmp_index:
        #     print(i)
        data.drop(data.index[i], inplace=True)
        data.index = range(len(data))  # 인덱스를 새롭게 매기는? 코드
    data.drop(data.index[index - len(tmp_index)::], inplace=True)

    dict1 = {}
    weeks = ['월', '화', '수', '목', '금']
    for i, ch in enumerate(data['time']):
        for j in range(len(data['time'][i])):
            if ch[j] in weeks:
                data['time'][i] = ch.strip()
                if ch[j] not in dict1:
                    dict1[ch[j]] = list()  # ch[j]키가 없을떈 빈리스트를 value로 하고, ch[j]를 키값으로 하는 요소생성
                if len(data['time'][i]) > 31:  # 일주일에 2번 나눠서 수업
                    if j > 1:
                        dict1[data['time'][i][0:j][0]].append([data['name'][i], data['time'][i][0:j]])
                        dict1[ch[j]].append([data['name'][i], data['time'][i][j:]])
                else:  # 일주일에 1타임만 수업
                    dict1[ch[j]].append([data['name'][i], data['time'][i]])

    for ch in dict1.keys():
        for i in range(len(dict1[ch])):
            list2 = dict1[ch][i][1].split(' ')
            if len(list2) > 2:
                if list2[2] != '':
                    dict1[ch][i][1] = list2[2]
                else:
                    dict1[ch][i][1] = list2[5]
            else:
                dict1[ch][i][1] = list2[0]

        dict1[ch] = sorted(dict1[ch], key=lambda x: x[1])

    dict2 = {}
    for ch in dict1.keys():
        dict2[ch] = dict1[ch][0][1][0:5]
        dict2[ch] = {'hour': int(dict2[ch][0:2]), 'minute': int(dict2[ch][3:5])}

    return [dict1,dict2]
if __name__ == "__main__":
    print(eclass(2019152015,"hoho1023!")[1]['월'])
