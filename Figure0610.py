# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import random   


#定义随机生成颜色函数
def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color ="#"+''.join([random.choice(colorArr) for i in range(6)])
    return color

# lims = [(np.datetime64('2005-02'), np.datetime64('2005-04')),
#         (np.datetime64('2005-02-03'), np.datetime64('2005-02-15')),
#         (np.datetime64('2005-02-03 11:00'), np.datetime64('2005-02-04 13:20'))]


os.chdir('D:\OneDrive - whu.edu.cn\桌面')
data = pd.read_excel("123.xlsx",sheet_name='Sheet2',skiprows=2)
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
# 将时间列转换为 datetime64[ns] 类型
df['hour'] = pd.to_datetime(df['hour'], format='%H:%M:%S').dt.time
# 合并日期列和时间列为一个日期时间列
df['Datetime'] = df['date'] + pd.to_timedelta(df['hour'].astype(str))
df = df.iloc[:, 2:]

#选取使用的数据
x=df.iloc[:,-1]#datetime
y=df.iloc[:,:-1]
labels=y.columns

# 获取列数
num_columns = y.shape[1]
#y=df.iloc[0:,2:-2].values 切片



#########################################################################################作图
fig, ax = plt.subplots(figsize=(10, 6),dpi=400,constrained_layout=True)#constrained_layout=True,去除白边有问题
plt.ylabel('Electricity Demand&Supply [GW]')


labels_1=['Nuclear','Fire','Hydro','Geothermal','Biomass','Wind','Solar','Pumped Hydro(Discharge)']
labels_2=['Export','Pumped Hydro(Charge)']
colors_1=['#C00000','#7F7F7F','#026FC4','#FF0508','#99BC56','#00B6EB','#FFC001','#093865']
colors_2=['#800080','#000078']
labels_3='Regional Demand'
colors_3=['#800080']
ax.stackplot(x,y['Nuclear'],y['Fire'],y['Hydro'],y['Geothermal'],y['Biomass'],y['Wind'],y['Solar'],y['Discharge'],labels=labels_1,colors=colors_1,zorder=100)
ax.stackplot(x,y['Export'],y['Charge'],labels=labels_2,colors=colors_2,zorder=100)
ax.plot(x,df['Demand'],color='#000000', label = labels_3,linewidth=2,linestyle='dashed',zorder=100)

##############################################太阳光制御
energy_total=y['Nuclear']+y['Fire']+y['Hydro']+y['Geothermal']+y['Biomass']+y['Wind']+y['Solar']+y['Discharge']
solar_control=energy_total-df['Solar(curtailed)']
ax.plot(x,energy_total,color='#FFFFFF',zorder=100) 
ax.plot(x,solar_control,color='#000000',zorder=100)
ax.fill_between(x,energy_total ,solar_control,hatch='\\',alpha=0,label='Solar(Curtailed)',zorder=100)

#################################################调整图例位置
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width , box.height* 0.8])
# ax.legend(loc='center left', bbox_to_anchor=(0, 1.06),ncol=6,fontsize=8)
ax.legend(loc='center left', bbox_to_anchor=(0, 1.06),ncol=6,fontsize=8)

# #################################################修正x轴密度
# ticker_spacing = 15 # 这个是x轴数据的显示间隔
# ax.plot(x,y)
# ax.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
# plt.xticks(rotation = 45)# 下面的rotation表示的是旋转角度
# ————————————————
##################################################修正x轴密度
ticklabels=['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00'
            ,'17:00','18:00','19:00','20:00','21:00','22:00','23:00']#设置x刻度

#TODO:plt.xlim([pd.to_datetime('2019-09-01 00:00'), pd.to_datetime('2019-09-01 00:04')])


plt.xticks(x,ticklabels,rotation = 45)
plt.xlim(x[0], x[23])

plt.grid(True, alpha=0.5,zorder=0)
plt.tight_layout()
plt.show()



#一个一个循环堆叠画图
# for i in range(num_columns):
#     ax.stackplot(x,y[labels[i]],baseline='sym',color=randomcolor())
#     if labels[i]=='Demand':
#         break
# plt.show



