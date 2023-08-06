def subTime(hour, minute, inja):
    cm = hour * 60 + minute - inja
    h = cm // 60
    m = cm % 60
    return h, m