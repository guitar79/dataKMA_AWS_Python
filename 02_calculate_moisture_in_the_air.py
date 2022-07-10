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


df['dt_YmdHM'] = pd.to_datetime(df['일시'])

from datetime import timedelta
df['dt_YmdHM-1min'] = df['dt_YmdHM'] - timedelta(minutes = 1)
df.index = df['dt_YmdHM-1min']
df


from metpy.units import units as u

v_distance = 8*u.m
v_time = 3*u.s

average_velocity = v_distance / v_time
average_velocity

"""type 함수로 어떤 데이터가 들어 있는지 확인해 보자. Quantity 가 들어 있음을 알 수 있다."""

print("type(v_distance):{}".format(type(v_distance )))
print("type(average_velocity):{}".format(type(average_velocity)))

"""string format을 이용하여 소수점 자리수를 설정할 수도 있다."""

"{0:0.03f}".format(average_velocity)

"""# Using metpy.calc

수증기의 열역학을 계산할 수 있는 [metpy.calc](https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html?highlight=calc#module-metpy.calc) 함수의 정보를 확인해 보자. 

metpy.calc 함수들은 dataframe 컬럼으로 계산을 하지 못하고, 단위를 포함한 pint.Quantity 객체를 변수로 입력해서 계산을 하도록 설계가 되어있다.

## 이슬점 온도 (dewpoint temperature)

먼저 이슬점 온도를 구해보자. dewpoint_from_relative_humidity 함수는 기온과 상대습도로 이슬점 온도를 구해준다. df의 특정 인덱스와 컬럼을 지정하여 특정한 날의 기온과 상대습도를 불러 보자.
"""

t_A = df.loc["2019-08-15 01:00", "기온(°C)"]
rh_A = df.loc["2019-08-15 01:00", "습도(%)"]

print("t_A: {}".format(t_A))
print("rh_A: {}".format(rh_A))

print("type(t_A): {}".format(type(t_A)))
print("type(rh_A): {}".format(type(rh_A)))

"""float type으로 저장되어 있는 데이터를 metpy.unit 함수를 이용하여 pint.Quantity로 변환해 주자."""

from metpy.units import units as u

t_A = df.loc["2019-08-15 01:00", "기온(°C)"] * u.degC
rh_A = df.loc["2019-08-15 01:00", "습도(%)"] * u.percent

print("t_A: {}".format(t_A))
print("rh_A: {}".format(rh_A))

print("type(t_A): {}".format(type(t_A)))
print("type(rh_A): {}".format(type(rh_A)))

"""이제 dewpoint_from_relative_humidity 함수를 이용하여 이슬점 온도를 구할 수 있다."""

import metpy.calc as mpcalc
from metpy.units import units as u

t_A = df.loc["2019-08-15 01:00", "기온(°C)"] * u.degC
rh_A = df.loc["2019-08-15 01:00", "습도(%)"] * u.percent

dewpoint_A = mpcalc.dewpoint_from_relative_humidity(t_A, rh_A)

print("공기덩이 A의 기온(°C): {}".format(t_A))
print("공기덩이 A의 습도(%): {}".format(rh_A))
print("공기덩이 A의 이슬점 온도(°C): {}".format(dewpoint_A))
print("type(dewpoint_A): {}".format(type(dewpoint_A)))

print("type(dewpoint_A): {}".format(type(dewpoint_A)))

"""다음과 같이 출력해 볼 수도 있을 것 같다."""

print('The magnitude of dewpoint temperature is {0.magnitude} with units {0.units}'.format(dewpoint_A))

"""## 혼합비(mixing ratio)

혼합비(Mixing Ratio)는 건조 공기 $1 \rm{~kg}$에 들어 있는 수증기의 양을 $ \rm{~g}$으로 나타낸 것이다.
        
$$ {\displaystyle	{
    \text { 혼합비 }=\frac{\text { 수증기 질량 }(\mathrm{g})}{\text { 건조 공기 질량 }(\mathrm{kg})} 
} 		} 	$$		

$$ {\displaystyle	{
    M.R.=\frac{m_{w}}{m_{d}}=\frac{\rho_{w}}{\rho_{d}} = 622 \frac{e}{p-e}(\mathrm{g} / \mathrm{kg})
} 		} 	$$		

이상기체 상태방정식을 이용해 구해볼 수 있다.
$$ {\displaystyle	{
    \begin{aligned}
        p&=\rho R T, \quad \rho=\frac{p}{R T} \\
        e&=\rho_w R_w T, \quad \rho_w=\frac{e}{R_w T} \\
        M.R.&=\frac{\rho_w}{\rho_d} = \frac{\frac{e}{R_w T}}{\frac{\left(p-e\right)}{R_d T}} = \frac{M_w}{M_d}\frac{e}{p-e}
    \end{aligned}
}	} $$

혼합비를 구하려면 기압값을 알아야 한다. 현지기압값이 Nan으로 되어 있는데, 아마 측정을 하지 않은 것으로 생각된다. 이 값을 1000으로 입력하자.
"""

p_A = 1000 *u.hPa

"""matpy.calc로 혼합비를 구해보자. """

print(p_A, t_A, rh_A)
mixing_ratio_A = mpcalc.mixing_ratio_from_relative_humidity(p_A, t_A, rh_A)
print("공기덩이 A의 혼합비: {:02f}".format(mixing_ratio_A))
mixing_ratio_A.magnitude

"""## 비습(specific humidity)

비습(Specific Humidity)은 수증기와 혼합되어 있는  $1 \rm{~kg}$에 들어 있는 수증기의 양을 $ \rm{~g}$으로 나타낸 것이다. 

$$ {\displaystyle	{
    \begin{aligned}
        &\text { 비습 }=\frac{\text { 수증기 질량 }(\mathrm{g})}{\text { 습윤 공기 질량 }(\mathrm{kg})} \\
        &S.H. = \frac{m_{w}}{m_{d}+m_{w}}=\frac{\rho_{w}}{\rho_{d}+\rho_{w}} = 622 \frac{e}{p}(\mathrm{g} / \mathrm{kg}) 
    \end{aligned}
}	} 	$$	


matpy.calc로  비습을 구해보자.
"""

print(p_A, dewpoint_A)
specific_humidity_A = mpcalc.specific_humidity_from_dewpoint(p_A, dewpoint_A)
print("공기덩이 A의 비습: {:02f}".format(specific_humidity_A))

"""## 수증기압(vaper pressure)

위의 결과로 수증기압을 구해보자.
"""

print(p_A, mixing_ratio_A)
vapor_pressure_A = mpcalc.vapor_pressure(p_A, mixing_ratio_A)
print("공기덩이 A의 수증기압: {:02f}".format(vapor_pressure_A))

"""## 습구 온도(wet bulb temperature)

습구 온도는 다음과 같이 구해볼 수 있다.

"""

print(p_A, t_A, dewpoint_A)
wet_bulb_temperature_A = mpcalc.wet_bulb_temperature(p_A, t_A, dewpoint_A)
print("공기덩이 A의 습구 온도: {:02f}".format(wet_bulb_temperature_A))

"""## 절대 습도(absolute humidity)

혼합공기 $1 \rm{~m^3}$에 들어있는 수증기의 양을 $\rm{g}$으로 나타낸 것으로 다음과 같이 구할 수 있다. 
$$ {\displaystyle	{
    \text { 절대습도 }=\frac{\text { 수증기 질량 }(\mathrm{g})}{\text { 공기 부피 }\left(\mathrm{m}^{3}\right)} 
}	}$$
				
이상기체 상태방정식으로 밀도를 구하면 
$$ {\displaystyle	{
    e = {\rho} R T, \quad \rho = \frac{e}{R T}
}	} $$
와 같다. 수증기의 밀도($\rho_w$)는 
$$ {\displaystyle	{
    \rho_{v}=\frac{e}{R_v T}
} 	} $$
$$ {\displaystyle	{
    \begin{aligned}
    R = M {\bar {R}} &= 8.3144 \left(\rm J~mol^{-1}~K^{-1}\right)  \\
				&= 8.3144 \left(\rm Pa~m^3~mol^{-1}~K^{-1}\right)
				\end{aligned}
}	}	$$

특별기체상수(specific gas constant)는 보편기체상수(${\bar{R}}$)를 기체의 분자량$\left(M\right)$으로 나누어 구할 수있다. 
$$ {\displaystyle	{
    R = \frac{\bar{R}}{M}
}	}	$$
수증기의 기체상수는
$$ {\displaystyle	{
    {{R_v}}={\frac {R}{M_v}} = {\frac {8.3144}{18}} = 0.461 \left(\rm J~g^{-1}~K^{-1}\right)
}	}$$

$$ {\displaystyle	{
    A. H.= \rho_{v}=\frac{e}{R_v T} = 217 \frac{e}{T} \left(\mathrm{g}~\mathrm{m}^{-3}\right)
} 		} 	$$
단, 여기에서 $\mathrm{e}: \mathrm{hPa}$, $\mathrm{T}: \mathrm{K}$ 단위이다.

## (과제)

metpy.calc에 절대습도를 구하는 함수는 존재하지 않는다. 위의 식을 이용하여 다음과 같이 절대습도를 구하는 함수를 직접 만들어 보자.

* 함수 이름 : absolute_humidity_from_vapor_pressure
* 입력 변수1 : #vapor preuusure (pint.Quantity) – hectopascal
* 입력 변수2 : #temperature (pint.Quantity) – degree_Celsius
* 출력 : #absolute humidity (pint.Quantity) – gram/meter3

함수를 만든 후 공기덩이 A의 절대습도를 구해보자.
"""

# 이곳에 코딩을 완성하여 제출하시오.

def absolute_humidity_from_vapor_pressure(vapor_pressure, temprature) :
    ####################################
    #Calculate the absolute humidity.
    #Uses vapor pressure(hPa) and temperature(degC) to calculate absolute humidity
    #Parameters
    #vapor preuusure (pint.Quantity) – hectopascal
    #temperature (pint.Quantity) – degree_Celsius
    #
    #Returns : absolute humidity (pint.Quantity) – gram/meter3
    ah = (18/8.3144)*u.g *u.degK /(u.N*u.m) * (vapor_pressure.to(u.Pa).to(u.N/((u.m)*(u.m)))) / temprature.to(u.degK)
    return ah

absolute_humidity_from_vapor_pressure(vapor_pressure_A, t_A)

"""# dataframe과 metpy.calc

아래 셀은 dataframe 컬럼으로 계산을 시도해 본 것인데, metpy.calc 함수들은 dataframe 컬럼으로 계산을 하지 못하고, 단위를 포함한 pint.Quantity 객체를 변수로 입력해서 계산을 하도록 설계가 되어있다.
"""

df['dewpoint_A'] = mpcalc.dewpoint_from_relative_humidity(df["기온(°C)"].values* u.degC, 
                                                        df["습도(%)"].values* u.percent)

"""## for ~ loop 문을 이용한 처리 

그래서 어쩔수 없이 속도는 느리지만 한 행마다 자료를 읽어서 for ~ loop문으로 처리를 해 보자. dataframe의 한 행씩 for ~loop를 할때는 df.iterrows()를 사용할 수 있다. 

"""

import metpy.calc as mpcalc
from metpy.units import units as u
    
for idx, row in df.iterrows():
    print("idx: {}".format(idx))
    print("row: {}".format(row))
    print("row['기온(°C)']: {}".format(row['기온(°C)']))
    break

"""dataframe의 각행에서 값을 읽어 단위를 곱한 후에 metpy.calc 함수를 이용하여 원하는 물리량을 계산한 후, 해당 행에 저장할 수 있다. 

해당 행에 저장하는 방법은 다음과 같다. 

> df.at[idx, "T_d"] = 

아래는 이슬점 온도를 구하여 저장하는 코드이다. 1달 동안의 모든 자료를 한줄씩 계산해야 하므로 시간이 좀 걸릴 것이다.
"""

import metpy.calc as mpcalc
from metpy.units import units as u
    
for idx, row in df.iterrows():
    
    #for debug
    #print(idx, row)
    #print("df.loc[idx, '기온(°C)']*u.degC: {}".format(df.loc[idx, '기온(°C)']*u.degC))
    #print("df.loc[idx, '습도(%)']*u.percent: {}".format(df.loc[idx, '습도(%)']*u.percent))
    #print("type(df.loc[idx, '기온(°C)']*u.degC): {}".format(type(df.loc[idx, '기온(°C)']*u.degC)))
    #print("type(df.loc[idx, '습도(%)']*u.percent: {}".format(type(df.loc[idx, '습도(%)']*u.percent)))

    df.at[idx, "T_d"] = mpcalc.dewpoint_from_relative_humidity(df.loc[idx, '기온(°C)'] *u.degC, 
                                                            df.loc[idx, '습도(%)'] *u.percent).magnitude          
                                                                
    print("idx, df.loc[idx, 'T_d']: {}, {}".format(idx, df.loc[idx, 'T_d']))

df

"""## dataframe 체크해 보기

특정 시간의 특정 데이터가 비어 있으면 계산을 하지 못할 수 있기 때문에 각 컬럼에서 비어 있는 자료가 있는지 체크해 볼 필요가 있겠다. 

series로 반환하여 s.isnull() method를 사용하면 bool 값을 반환해 주는데, 갯수를 알고 싶으면 s.isnull()sum()으로 합을 구해보면 될 것이다. 
"""

print("df['기온(°C)'].isnull(): {}".format(df['기온(°C)'].isnull()))
print("df['기온(°C)'].isnull().sum(): {}".format(df['기온(°C)'].isnull().sum()))
print("df['습도(%)'].isnull().sum(): {}".format(df['습도(%)'].isnull().sum()))

"""'습도(%)' 컬럼에서 213개의 행에 자료가 없는 것이 확인되었다. 자료가 없는 것을 제외한 subset을 만들어 보자."""

df.dropna(axis=0,subset=['기온(°C)', '습도(%)'])['기온(°C)']
df.dropna(axis=0,subset=['기온(°C)', '습도(%)'])['습도(%)']
df.dropna(axis=0,subset=['기온(°C)', '습도(%)'])

print(len(df))
print(len(df.dropna(axis=0,subset=['기온(°C)', '습도(%)'])))

"""subset을 이용하여 다시 for ~ loop를 돌려보는 방법도 있다. """

import metpy.calc as mpcalc
from metpy.units import units as u
    
for idx, row in df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).iterrows():
    
    #for debug
    #print(idx, row)
    #print("df.loc[idx, '기온(°C)']*u.degC: {}".format(df.loc[idx, '기온(°C)']*u.degC))
    #print("df.loc[idx, '습도(%)']*u.percent: {}".format(df.loc[idx, '습도(%)']*u.percent))
    #print("type(df.loc[idx, '기온(°C)']*u.degC): {}".format(type(df.loc[idx, '기온(°C)']*u.degC)))
    #print("type(df.loc[idx, '습도(%)']*u.percent: {}".format(type(df.loc[idx, '습도(%)']*u.percent)))

    df.at[idx, "T_d"] = mpcalc.dewpoint_from_relative_humidity(df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, '기온(°C)'] *u.degC, 
                                                            df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, '습도(%)'] *u.percent).magnitude          
                                                                
    print("idx, df.loc[idx, 'T_d']: {}, {}".format(idx, df.loc[idx, 'T_d']))
    break 
    
df

"""## error handling

for ~ loop 문이 실행되는 동안에 error가 발생하면 loop가 중단된다. error가 발생하더라도 loop가 중단되지 않게 하려면 다음과 같이 하는 방법도 있다.
"""

import metpy.calc as mpcalc
from metpy.units import units as u

for idx, row in df.iterrows():
    try :
        #for debug
        #print(idx)
        
        #print("df.loc[idx, '기온(°C)']*u.degC: {}".format(df.loc[idx, '기온(°C)']*u.degC))
        #print("df.loc[idx, '습도(%)']*u.percent: {}".format(df.loc[idx, '습도(%)']*u.percent))
        #print("type(df.loc[idx, '기온(°C)']*u.degC): {}".format(type(df.loc[idx, '기온(°C)']*u.degC)))
        #print("type(df.loc[idx, '습도(%)']*u.percent: {}".format(type(df.loc[idx, '습도(%)']*u.percent)))
        #print(mpcalc.dewpoint_from_relative_humidity(df.loc[idx, '기온(°C)']*u.degC, df.loc[idx, '습도(%)']*u.percent))
        #print(type(mpcalc.dewpoint_from_relative_humidity(df.loc[idx, '기온(°C)']*u.degC, df.loc[idx, '습도(%)']*u.percent)))
                                                         
        df.at[idx, 'T_d'] = mpcalc.dewpoint_from_relative_humidity(df.loc[idx, '기온(°C)']*u.degC, 
                                                        df.loc[idx, '습도(%)']*u.percent).magnitude
        print("idx, df.loc[idx, 'T_d']: {}, {}".format(idx, df.loc[idx, 'T_d']))
        break                                                   
        
    except Exception as err: 
        print("{} error :{}".format(idx, err))
        break 

df

"""subset과 error handling 을 모두 적용한 것이다."""

import metpy.calc as mpcalc
from metpy.units import units as u

for idx, row in df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).iterrows():
    try :
        #for debug
        #print(idx)
        #print(idx, row)
        #print("df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, '기온(°C)']*u.degC: {}".format(df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, '기온(°C)']*u.degC))
        #print("df.loc[idx, '습도(%)']*u.percent: {}".format(df.loc[idx, '습도(%)']*u.percent))
        #print("type(df.loc[idx, '기온(°C)']*u.degC): {}".format(type(df.loc[idx, '기온(°C)']*u.degC)))
        #print("type(df.loc[idx, '습도(%)']*u.percent: {}".format(type(df.loc[idx, '습도(%)']*u.percent)))
        #print(df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, '기온(°C)'] *u.degC)
        
        df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).at[idx, "T_d"] =  \
                        mpcalc.dewpoint_from_relative_humidity(df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, '기온(°C)']*u.degC, \
                        df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, '습도(%)']*u.percent).magnitude
                                                                    
        print("idx, df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, 'T_d']: {}, {}".format(idx, df.dropna(axis=0,subset=['기온(°C)', '습도(%)']).loc[idx, 'T_d']))
        break 

    except Exception as err: 
        print("{} error :{}".format(idx, err))
        break 
        
df

"""## 기압값 입력 

AWS 자료에는 해면기압(hPa) 값이 NaN 이다. 할수 없이 기압을 1000 hPa로 정해서 dataframe에 입력해 보자. 
"""

df['현지기압(hPa)'] = 1000
df

"""## (과제)

위의 예제를 응용하여 다음의 물리량들을 계산하여 dataframe에 새로운 컬럼에 입력해 보자.

* 이슬점 온도 : 'T_d(°C)'
* 혼합비 : 'MR(unitless)'
* 비습 : 'SH(unitless)'
* 수증기압 : 'VP(hPa)'
* 습구온도 : 'T_wb(°C)' (현재는 에러로 산출 불가함.)
* 절대 습도 : 'AH(g/cm^3)'
"""

#(과제) 아래에 코딩을 완성하여 제출하시오.

import metpy.calc as mpcalc
from metpy.units import units as u
    
for idx, row in df.iterrows():
    try :
        #for debug
        #print(idx, row)
        
        #이슬점 온도
        df.at[idx, 'T_d(°C)'] = mpcalc.dewpoint_from_relative_humidity(df.loc[idx, '기온(°C)']*u.degC, 
                                            df.loc[idx, '습도(%)']*u.percent).magnitude
        #print("T_d(°C)")
        print("idx, df.loc[idx, 'T_d(°C)']: {}, {}".format(idx, df.loc[idx, 'T_d(°C)']))

        # 혼합비
        df.at[idx, 'MR(unitless)'] = mpcalc.mixing_ratio_from_relative_humidity(df.loc[idx, '현지기압(hPa)']*u.hPa, 
                                            df.loc[idx, '기온(°C)']*u.degC, 
                                            df.loc[idx, '습도(%)']*u.percent).magnitude
        #print("MR(unitless)")
        print("idx, df.loc[idx, 'MR(unitless)']: {}, {}".format(idx, df.loc[idx, 'MR(unitless)']))

        #비습 
        df.at[idx, 'SH(unitless)'] = mpcalc.specific_humidity_from_dewpoint(df.loc[idx, '현지기압(hPa)']*u.hPa, 
                                            df.loc[idx, 'T_d(°C)']*u.degC).magnitude
        #print("SH(unitless)")
        print("idx, df.loc[idx, 'SH(unitless)']: {}, {}".format(idx, df.loc[idx, 'SH(unitless)']))
        
        #수증기압 
        df.at[idx, 'VP(hPA)'] = mpcalc.vapor_pressure(df.loc[idx, '현지기압(hPa)']*u.hPa, 
                                            df.loc[idx, 'MR(unitless)']).magnitude
        #print("VP")
        print("idx, df.loc[idx, 'VP(hPA)']: {}, {}".format(idx, df.loc[idx, 'VP(hPA)']))

        #습구 온도 
        #for debug
        #print(type(df.loc[idx, '현지기압(hPa)']))
        #print(type(df.loc[idx, '기온(°C)']))
        #print(type(df.loc[idx, 'T_d(°C)']))
        #print(df.loc[idx, '현지기압(hPa)']*u.hPa)
        #print(df.loc[idx, '기온(°C)']*u.degC)
        #print(df.loc[idx, 'T_d(°C)']*u.degC)
        #print(type(df.loc[idx, '현지기압(hPa)']*u.hPa))
        #print(type(df.loc[idx, '기온(°C)']*u.degC))
        #print(type(df.loc[idx, 'T_d(°C)']*u.degC))
        #print(mpcalc.wet_bulb_temperature(df.loc[idx, '현지기압(hPa)']*u.hPa, 
        #                                  df.loc[idx, '기온(°C)']*u.degC, 
        #                                  df.loc[idx, 'T_d(°C)']*u.degC).magnitude)
        #df.at[idx, 'T_wb(°C)'] = mpcalc.wet_bulb_temperature(df.loc[idx, '현지기압(hPa)']*u.hPa, 
        #                                    df.loc[idx, '기온(°C)']*u.degC, 
        #                                    df.loc[idx, 'T_d(°C)']*u.degC).magnitude
        #print("T_wb(°C)")
        #print("idx, df.loc[idx, 'T_wb(°C)']: {}, {}".format(idx, df.loc[idx, 'T_wb(°C)']))        
        
        #절대 습도
        df.at[idx, 'AH(g/cm^3)'] = absolute_humidity_from_vapor_pressure(df.loc[idx, 'VP(hPA)']*u.hPa, 
                                            df.loc[idx, '기온(°C)']*u.degC).magnitude
        #print("AH")
        print("idx, df.loc[idx, 'AH(g/cm^3)']: {}, {}".format(idx, df.loc[idx, 'AH(g/cm^3)']))
        #break

    except Exception as err: 
        print("{} error :{}".format(idx, err))
        #break

df

"""이제 dataframe을 csv 파일로 저장해 보자."""

df

df.to_csv("{}_result.csv".format(filename[:-4]))
print("{}_result.csv is created...".format(filename[:-4]))