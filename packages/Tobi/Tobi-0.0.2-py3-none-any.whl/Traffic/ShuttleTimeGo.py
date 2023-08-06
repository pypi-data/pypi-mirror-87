def shuttleTimeGo(hour, minute, dict_go):
    # defhour, defminute이 선언되지 않아서 if문에서 조건을 충족하지 못해서
    # defhour이 원하는 값으로 초기화되지 않은 경우 초기화된 값이 없으므로 return에서 오류(UnboundLocalError) 발생
    defhour = int(hour)
    defminute = int(minute)
    convminute = int(minute) + 60 * int(hour)
    while (True):
        if (8 <= defhour <= 22):
            if (int(dict_go[defhour][0]) + defhour * 60 + 15 > convminute):
                # 셔틀시간+15분이 학교에 도착하는 시간이라는 가정하에,시간대에 가장 이른 셔틀의 도착시간은 defminute보다 크면 안됨,
                defhour -= 1
                # 따라서 defhour을 1 빼주고
                continue
                # defminute를 60으로 설정.
                # 반복문의 맨 처음으로 돌아가게 한다.
            else:
                for i in range(len(dict_go[defhour])):
                    if (convminute >= int(dict_go[defhour][-1 - i]) + defhour * 60 + 15):
                        defminute = dict_go[defhour][-1 - i]
                        return (str(defhour), str(defminute))
                    else:
                        continue
        else:
            return ("err", "err")

