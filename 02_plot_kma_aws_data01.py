#package 불러오기
from calendar import weekday
import pandas as pd

#데이터가 저장되어 있는 폴더명 설정
base_dr = '../SURFACE_AWS_data_unzip/'

filename = 'SURFACE_AWS_425_MI_2015-01_2015-01_2018.csv'

#파일을 읽어들여

from glob import glob
import os

fullnames = sorted(glob(os.path.join(base_dr, 'SURFACE_AWS_425_MI_2015*.csv')))
print("fullnames : {}".format(fullnames))

# 빈 DataFrame 생성
df = pd.DataFrame()

for fullname in fullnames :
    df_month = pd.read_csv('{0}'.format(fullname),
                 thousands = ',',
                 encoding= 'euc-kr')
    df = df.append(df_month)

df


df.head()

df.tail()

df.describe()

len(df)

df['dt_YmdHM'] = pd.to_datetime(df['일시'])
df

print("type(df['dt_YmdHM'][0]):{}".format(type(df['dt_YmdHM'][0])))

df.index = df['dt_YmdHM']
df


from datetime import timedelta
df['dt_YmdHM-1min'] = df['dt_YmdHM'] - timedelta(minutes = 1)
df.index = df['dt_YmdHM-1min']
df

###################################

import metpy.calc as mpcalc
from metpy.units import units as u

df['T_d(°C)'] = mpcalc.dewpoint_from_relative_humidity(df['기온(°C)']*u.degC, 
                                            df['습도(%)']*u.percent)
 
for idx, row in df.iterrows():
    try :
        #for debug
        print(idx, row)
        #이슬점 온도
        df.at[idx, 'T_d(°C)'] = mpcalc.dewpoint_from_relative_humidity(df.loc[idx, '기온(°C)']*u.degC, 
                                            df.loc[idx, '습도(%)']*u.percent).magnitude
        #print("T_d(°C)")
        print("idx, df.loc[idx, 'T_d(°C)']: {}, {}".format(idx, df.loc[idx, 'T_d(°C)']))
 
    except Exception as err: 
        print("{} error :{}".format(idx, err))
        break 
        
df


df['현지기압(hPa)'] = 1000
df

###############################################

df_1day = df[(df['dt_YmdHM-1min'] >= '2015-01-01 00:00') & (df['dt_YmdHM-1min'] < '2015-01-02 00:00')]
df_1day


start_date = min(df['dt_YmdHM-1min'])
end_date = min(df['dt_YmdHM-1min'])  + timedelta(days = 1)

while start_date < (max(df['dt_YmdHM-1min'] - timedelta(days = 0))) :

    #df_7days = df[(df['dt_YmdHM-1min'] >= '2015-01-01 00:00') & (df['dt_YmdHM-1min'] < '2015-01-08 00:00')]
    end_date = start_date  + timedelta(days = 1)

    df_7days = df[(df['dt_YmdHM-1min'] >= start_date) & (df['dt_YmdHM-1min'] < end_date)]


    ## 이곳에 코딩을 완성하세요.
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime, timedelta
    import matplotlib.dates as dates
    import matplotlib.ticker as ticker

    # Colab 의 한글 폰트 설정
    plt.rc('font', family='NanumBarunGothic') 

    # 그림 사이즈를 가로로 길게 지정
    fig, ax1 = plt.subplots(figsize=(10, 8))

    #기온 그래프
    Temp_line = ax1.plot(df_7days['dt_YmdHM-1min'], 
                        df_7days['기온(°C)'], 'r-', label='temperature')

    #가로축1
    ax1.set_xlabel('day, Hour', fontsize = 14)
    ax1.grid(which='both', axis='x')
    #범위 지정
    ax1.set_xlim(min(df_7days['dt_YmdHM-1min']), 
                max(df_7days['dt_YmdHM-1min']))
    #날짜시간 포멧
    ax1.xaxis.set_major_locator(dates.DayLocator())
    ax1.xaxis.set_minor_locator(dates.HourLocator(interval=6))
    ax1.xaxis.set_major_formatter(dates.DateFormatter('%d, %Hh'))
    ax1.xaxis.set_minor_formatter(dates.DateFormatter('%d, %Hh'))

    #세로축1
    ax1.set_ylabel('Temperature (°C)', fontsize = 14)
    ax1.tick_params('y', colors='r')
    #범위 지정
    ax1.set_ylim((int(min(df_7days['기온(°C)'])/10)-1)*10, 
                (int(max(df_7days['기온(°C)'])/10)+1)*10) # 10의 배수로 떨어지도록 변환

    #twinx() 이므로 제목은 하나만 써도 됨.
    ax1.set_title('{} - {}'.format(start_date, end_date), 
            y=1.05,   # margin under the title.
            fontdict={'fontsize':18,'fontweight':'bold'})

    # added these lines
    plt.legend()
    plt.savefig("{}T_chart/T_{}_{}.png".format(base_dr, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')))
    start_date += timedelta(days = 1)
    
    #세로축 추가
    ax2 = ax1.twinx()

    #습도 그래프
    Humi_line = ax2.plot(df_7days['dt_YmdHM-1min'], 
                        df_7days['습도(%)'], 'b-', label='humidity')

    #가로축2
    #범위 지정
    ax2.set_xlim(min(df_7days['dt_YmdHM-1min']), 
                max(df_7days['dt_YmdHM-1min']))
    #날짜시간 포멧
    ax2.xaxis.set_major_locator(dates.DayLocator())
    ax2.xaxis.set_minor_locator(dates.HourLocator(interval=6))
    ax2.xaxis.set_major_formatter(dates.DateFormatter('%d, %Hh'))
    ax2.xaxis.set_minor_formatter(dates.DateFormatter('%d, %Hh'))

    #세로축2
    ax2.grid(which='both', axis='both')
    ax2.set_ylabel('humidity (%)', fontsize = 14)
    ax2.tick_params('y', colors='b')
    ax2.set_ylim(0, 100)

    # added these lines
    lns = Temp_line + Humi_line
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs)
    
    plt.savefig("{}TH_chart/TH_{}_{}.png".format(base_dr, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')))
    start_date += timedelta(days = 1)
    
    #plt.show()
