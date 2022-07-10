# -*- coding: utf-8 -*-
# guitar79@naver.com
'''period,Year,JulianDay,Time,Air Temp(℃),RH(%),Wind Dir(Deg),Wind Spd<m/s),Gust(m/s),GustTime,Solar Rad(W/㎡),Pressure(hPa),Visibility(km),Rain(mm),,,,
#5,2010,1,5,-12.28,76.1,198.8,11.21,1.287,4,0.605,1023,12.79,0,,,,
#5,2010,1,10,-12.35,77.3,184.7,5.465,1,10,0.726,1023,12.77,0,,,,
'''
import numpy as np
import matplotlib.pyplot as plt

#읽어들일 aws_csv 파일 이름 지정
input_file = '../SURFACE_AWS_data_unzip/SURFACE_AWS_425_MI_2015-01_2015-01_2018.csv'
#파일을 읽어들여서 매 라인마다 ','로 구분하여 numpy array로 저장
aws_csv = np.genfromtxt (input_file, delimiter=",",  encoding='euc-kr')

#aws_csv라는 이름의 numpy array를 화면에 출력
print(aws_csv)

#aws_csv라는 이름의 numpy array에 들어 있는 갯수를 카운트하여 출력
total_record_number = len(aws_csv)
print('total record number: %s' %(total_record_number))

#해당 Julian day의 자료만 선택
aws_csv=aws_csv[aws_csv[:,2] == wday]

#해당 날짜의 자료 갯수를 출력
record_number = len(aws_csv)
print('record number of Julian day: %s' %(record_number))

#aws_csv라는 이름의 numpy array에 지정된 컬럼을 변수로 저장(0에서 시작함)
Jday = aws_csv[:,2]
Time = aws_csv[:,3]/100
Temp = aws_csv[:,4]
Humidi = aws_csv[:,5]

print("온도값들")
print(Temp)

print("습도 값들")
print(Humidi)

#그래프를 그려보자.
fig, ax1 = plt.subplots(figsize=(10,7))

#x축 레이블
ax1.set_xlabel('Time(24 Hour)')

#시간-온도 그래프 그림
ax1.plot(Time[1:288],Temp[1:288], 'b-', label='Temperature')

# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Temperature (℃)', color='b')
ax1.tick_params('y', colors='b')
plt.legend(loc='upper right', bbox_to_anchor=(1, 0.55))

#x축 간격조정 
plt.xlim(0,24)
#ax1.xticks(data, labels)
plt.ylim(-20, 10)

ax2 = ax1.twinx()
ax2.plot(Time[1:288],Humidi[1:288], 'r-', label='Relative Humidity')
ax2.set_ylabel('Humidity (%)', color='r')
ax2.tick_params('y', colors='r')
plt.ylim(0, 100)
plt.title('Julian day: %s' %(wday), fontsize=14)

plt.legend(loc='upper right', bbox_to_anchor=(1, 0.48))
#fig.suptitle('시간에 따른 기온과 습도의 변동')
fig.suptitle('Variation of temperature and humidity every 5 min', fontsize=18)


#plt를 png 파일과 pdf 파일로 저장
plt.savefig('5-min_Jday%s.png'%(wday))
plt.savefig('5-min_Jday%s.pdf'%(wday))

plt.show()
plt.close()