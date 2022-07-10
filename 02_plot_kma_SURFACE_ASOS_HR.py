#package 불러오기
from calendar import month, weekday
from codecs import utf_8_decode
from encodings import utf_8
from datetime import datetime, timedelta
import pandas as pd
from glob import glob
import os
import Python_utilities

log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))


#데이터가 저장되어 있는 폴더명 설정
base_dr = '../SURFACE_ASOS_data_HR/'
filename = 'SURFACE_ASOS_108_HR_2011_2011_2018.csv'
fullname = base_dr + filename

start_date = pd.Timestamp(1969, 5, 1, 0, 0, 0)

Site_code = "108"
Site_code = "133"
Site_code = "112"

chart_save_dr = "../chart_SURFACE_ASOS_data_Hr_TTdH/{}/".format(Site_code)
if not os.path.exists(chart_save_dr):
    os.mkdir(chart_save_dr)
    print("{} is created...".format(chart_save_dr))
    
"""
df = pd.read_csv('{0}'.format(fullname),
                 thousands = ',',
                 encoding= 'euc-kr')
"""

#파일을 읽어들여
fullnames = sorted(glob(os.path.join(base_dr, 'SURFACE_*{}_*.csv'.format(Site_code))))
print("fullnames : {}".format(fullnames))

# 빈 DataFrame 생성
df = pd.DataFrame()

for fullname in fullnames :
    df_month = pd.read_csv('{0}'.format(fullname),
                 thousands = ',',
                 encoding= 'euc-kr')
    df = df.append(df_month)

# print df
print("df: {}".format(df))

print("df.head(): {}".format(df.head()))
print("df.tail(): {}".format(df.tail()))
print("df.describe(): {}".format(df.describe()))
print("len(df): {}".format(len(df)))


from datetime import timedelta
df['dt_YmdHM'] = pd.to_datetime(df['일시'])
df

#debug
#print("type(df['dt_YmdHM'][0]):{}".format(type(df['dt_YmdHM'][0])))

df.index = df['dt_YmdHM']
df = df.drop_duplicates()

#df = df.sort_index()
#df = df.dropna(axis=0,subset=['기온(°C)', '이슬점온도(°C)','습도(%)'])
#df = df.interpolate(method='time', axis=0)
#df

time_delta = 3

###############################################

while start_date < (max(df['dt_YmdHM'] - timedelta(days = 0))) :
#while start_date < (begin_date + timedelta(days = 10)) :

    #df_7days = df[(df['dt_YmdHM'] >= '2015-01-01 00:00') & (df['dt_YmdHM'] < '2015-01-08 00:00')]
    end_date = start_date  + timedelta(days = time_delta)
    
    ##
    print("start_date ~ end_date {} ~ {}".format(start_date, end_date))
    
    try : 
        df_7days = df[(df['dt_YmdHM'] >= (start_date)) & (df['dt_YmdHM'] <= end_date)]
        df_7days.to_csv("{}chart_{}_{}_{}.csv".format(chart_save_dr, Site_code, 
                                                start_date.strftime('%Y%m%d'), 
                                                end_date.strftime('%Y%m%d')),
                                                encoding="utf-8-sig")
        print("{}chart_{}_{}_{}.csv is created...".format(chart_save_dr, Site_code, 
                                                start_date.strftime('%Y%m%d'), 
                                                end_date.strftime('%Y%m%d')))
    
        if  os.path.exists("{}chart_{}_{}_{}.png".format(chart_save_dr, Site_code, 
                                                start_date.strftime('%Y%m%d'), 
                                                end_date.strftime('%Y%m%d'))) :
            print("{}chart_{}_{}_{}.png is already exist".format(chart_save_dr, Site_code, 
                                                start_date.strftime('%Y%m%d'), 
                                                end_date.strftime('%Y%m%d'))) 
        else : 
                
            ###
            #df_7days['기온(°C)'].interpolate(method='time') 
            #df_7days['이슬점온도(°C)'].interpolate(method='time') 
            #df_7days['습도(%)'].interpolate(method='time')
            #df_7days['기온(°C)', '이슬점온도(°C)', '습도(%)'].interpolate(method='time')  
            #df_7days = df_7days.interpolate(method='spline')    
            
            ## 
            import numpy as np
            import matplotlib.pyplot as plt
            import matplotlib.dates as dates
            import matplotlib.ticker as ticker

            # 그림 사이즈를 가로로 길게 지정
            fig, ax1 = plt.subplots(figsize=(15, 8))

            #기온 그래프
            #Temp_line = ax1.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['기온(°C)'], 'r-', label='temperature')
            Temp_dot = ax1.plot(df_7days['dt_YmdHM'], 
                                df_7days['기온(°C)'], 'ro',
                                markersize=3)
            #Td_line = ax1.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['이슬점온도(°C)'], 'g-', label='Dwe point temperature')
            Td_line = ax1.plot(df_7days['dt_YmdHM'], 
                                df_7days['이슬점온도(°C)'], 'go',
                                markersize=3)
            #Temp_line = ax1.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['기온(°C)'].interpolate(method='time'), 'r-', label='temperature')
            #Temp_dot = ax1.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['기온(°C)'], 'ro')
            #Td_line = ax1.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['이슬점온도(°C)'].interpolate(method='time'), 'g-', label='Dwe point temperature')
            
            #debug
            #print("len(df_7days['이슬점온도(°C)']): {}".format(len(df_7days['이슬점온도(°C)'])))
            #print("df_7days['이슬점온도(°C)']: {}".format(df_7days['이슬점온도(°C)']))

            #가로축1
            ax1.set_xlabel('day, Hour', fontsize = 16)
            ax1.grid(which='both', axis='x')
            #범위 지정
            ax1.set_xlim(start_date, end_date)
            #날짜시간 포멧
            ax1.xaxis.set_major_locator(dates.DayLocator(interval=1))
            ax1.xaxis.set_minor_locator(dates.HourLocator(interval=6))
            ax1.xaxis.set_major_formatter(dates.DateFormatter('%d %Hh'))
            ax1.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))

            #세로축1
            ax1.set_ylabel('Temperature (°C)', fontsize = 16)
            ax1.tick_params('y', colors='r')
            #범위 지정
            #ax1.set_ylim((int(min(df_7days['기온(°C)'])/10)-2)*10, 
            #            (int(max(df_7days['기온(°C)'])/10)+2)*10) # 10의 배수로 떨어지도록 변환
            
            ax1.set_ylim(-30, 50) 

            #twinx() 이므로 제목은 하나만 써도 됨.
            ax1.set_title('{}: {} days'.format(start_date.strftime('%Y-%m-%d'), time_delta), 
                    y=1.05,   # margin under the title.
                    fontdict={'fontsize':18,'fontweight':'bold'})
            

            # added these lines
            #plt.legend()
            #plt.savefig("{}T_chart/T_{}_{}.png".format(base_dr, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')))
            
            #세로축 추가
            ax2 = ax1.twinx()

            #습도 그래프
            #Humi_line  = ax2.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['습도(%)'], 'b-', label='Humidity')
            #Humi_line  = ax2.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['습도(%)'].interpolate(method='time'), 'b-', label='Humidity')
            Humi_dot  = ax2.plot(df_7days['dt_YmdHM'], 
                                df_7days['습도(%)'], 'bo',
                                markersize=3)
            #Humi_dot  = ax2.plot(df_7days['dt_YmdHM'], 
            #                    df_7days['습도(%)'].interpolate(method='time'), 'b*')
            
            print("len(df_7days['습도(%)']): {}".format(len(df_7days['습도(%)'])))
            #가로축2
            #범위 지정
            #ax2.set_xlim(min(df_7days['dt_YmdHM']), max(df_7days['dt_YmdHM']))
            ax2.set_xlim(start_date, end_date)
            #날짜시간 포멧
            ax2.xaxis.set_major_locator(dates.DayLocator(interval=1))
            ax2.xaxis.set_minor_locator(dates.HourLocator(interval=6))
            ax2.xaxis.set_major_formatter(dates.DateFormatter('%d %Hh'))
            ax2.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))

            #세로축2
            ax2.grid(which='both', axis='both')
            ax2.set_ylabel('Humidity (%)', fontsize = 16)
            ax2.tick_params('y', colors='b')
            ax2.set_ylim(0, 100)
            
            ######
            import matplotlib.dates as dates
            from scipy.interpolate import make_interp_spline
            # 300 represents number of points to make between T.min and T.max
            date_num = dates.date2num(df_7days.index)
            date_num_smooth = np.linspace(date_num.min(), date_num.max(), 500) 
            spl_temp = make_interp_spline(date_num, df_7days['기온(°C)'].interpolate(method='time'), k=3) 
            temp_smooth = spl_temp(date_num_smooth)
            Temp_interpolation = ax1.plot(date_num_smooth, temp_smooth , 'r-', label='temperature')
            
            spl_dew_temp = make_interp_spline(date_num, df_7days['이슬점온도(°C)'].interpolate(method='time'), k=3) 
            dew_temp_smooth = spl_dew_temp(date_num_smooth)    
            Td_interpolation = ax1.plot(date_num_smooth, dew_temp_smooth, 'g-', label='dwe point temperature')

            spl_humi = make_interp_spline(date_num, df_7days['습도(%)'].interpolate(method='time'), k=3) 
            humi_smooth = spl_humi(date_num_smooth)
            Humi_interpolation = ax2.plot(date_num_smooth, humi_smooth, 'b-', label='humidity')
            
            # added these lines
            #lns = Temp_line + Td_line + Humi_line
            lns = Temp_interpolation + Td_interpolation + Humi_interpolation
            labs = [l.get_label() for l in lns]
            plt.legend(lns, labs)
            
            plt.savefig("{}chart_{}_{}_{}.png".format(chart_save_dr, Site_code, 
                                                    start_date.strftime('%Y%m%d'), 
                                                    end_date.strftime('%Y%m%d')))
            print("{}chart_{}_{}_{}.png is created...".format(chart_save_dr, Site_code, 
                                                    start_date.strftime('%Y%m%d'), 
                                                    end_date.strftime('%Y%m%d')))
            plt.close()
            
    except Exception as err :
        print("X"*60)
        Python_utilities.write_log(err_log_file,
                    '{0} ::: {1} with {2}, {3}, {4}'\
                    .format(datetime.now(), err, Site_code, 
                                    start_date.strftime('%Y%m%d'), 
                                    end_date.strftime('%Y%m%d')))

    start_date += timedelta(days = 1)