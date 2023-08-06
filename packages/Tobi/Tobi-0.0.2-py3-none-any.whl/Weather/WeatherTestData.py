import pandas as pd

pd.options.display.float_format = '{:.1f}'.format  # 소수점 1자리만 나타내주는 코드
dt = pd.read_excel("test.xlsx")
dt['now_time'] = dt['now_time'].fillna(method='bfill')
dt['time'] = dt['time'].fillna(method='bfill')
print(dt)
print(dt.loc[dt['type']=='통합'][53::])