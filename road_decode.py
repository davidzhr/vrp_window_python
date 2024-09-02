import  numpy as  np
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
plt.rcParams['font.sans-serif']=['STSong'] #汉字是宋体
from data import  data_m

class tool():
    def __init__(self,load_max,car_v,parm_p):
         self.load_max=load_max      #载重
         self.car_v=car_v            #速度
         self.s1=parm_p[0]           #违反约束参数s1
         self.s2=parm_p[1]           #违反约束参数s2
         self.pi=parm_p[2]           #违反约束参数pi

    def decode(self, road):
        global location_xy
        da = data_m()
        location_xy, demand, time_window, distance = da.information()

        # 初始化每辆车途径的需求点、时间窗惩罚成本、路程、累计运行时间等
        car_road, car_p, car_s, car_time = [], [], [], []
        # 初始化每个站点对应的车的编码和需求量
        time, car_code, car_demand, car_window, car_distance, car_un = [], [], [], [], [], []
        signal = -1
        window_low = []

        # 遍历路径中的每个需求点
        for i in range(road.shape[0]):
            loc_index = int(road[i])
            # 当是第一个需求点或者车辆剩余载重小于需求量时
            if (i < 1) or (demand[loc_index] > car_load):
                # 当车辆剩余载重小于需求量时，更新车辆的路程和时间窗惩罚成本
                if (i > 0):
                    car_dis += distance[loc_index, 0]
                    time_car += distance[loc_index, 0] / self.car_v
                    time.append(time_car)
                    car_time[signal].append(time_car)  # 保存车辆累计运行时间
                    car_p.append(p)  # 保存车辆时间窗惩罚成本
                    car_s.append(car_dis)  # 保存该车辆路程

                    car_road[signal].append(0)
                    car_window[signal].append(0)
                    car_distance[signal].append(car_dis)
                    car_un[signal].append(0)
                # 初始化新车的载重、路径、时间窗、路程等
                car_load = self.load_max
                car_road.append([0])
                car_window.append([0])
                car_time.append([0])
                car_distance.append([0])
                car_un.append([0])
                signal += 1  # 一辆车装完后换下一辆
                car_dis = 0  # 初始化每辆车路程为0
                time_car = 0  # 初始化每辆车时间为0
                p = 0  # 初始化每辆车的时间窗惩罚成本为0
            # 更新每辆车剩余载重
            car_load -= demand[loc_index]
            car_road[signal].append(loc_index)
            car_code.append(signal)
            sig = car_road[signal][-2]
            svg = car_road[signal][-1]
            dis = distance[sig, svg]  # 计算每个需求点和上一个需求点的距离

            # 更新每辆车运行时间和距离
            time_car += dis / self.car_v
            car_dis += dis
            car_distance[signal].append(car_dis)
            car_demand.append(demand[loc_index])
            car_window[signal].append(time_window[loc_index])
            car_time[signal].append(time_car)

            # 计算时间窗惩罚成本
            Ai = time_window[loc_index, 0]
            Bi = time_window[loc_index, 1]
            window_low.append(Ai)
            Ei = Ai - self.pi * Ai
            Li = Bi + self.pi * Ai
            if (time_car <= Ei):
                loss = self.s1
                car_un[signal].append(1)
            if (time_car > Ei) and (time_car <= Ai):
                loss = (self.s1 / (Ai - Ei)) * (Ai - time_car)
                car_un[signal].append(0)
            if (time_car > Ai) and (time_car <= Bi):
                loss = 0
                car_un[signal].append(0)
            if (time_car > Bi) and (time_car <= Li):
                loss = (self.s2 / (Li - Bi)) * (time_car - Bi)
                car_un[signal].append(0)
            if (time_car > Li):
                loss = self.s2
                car_un[signal].append(2)
            p += loss  # 更新每辆车的时间窗惩罚成本

            # 最后一个点更新各个变量
            if (i == road.shape[0] - 1):
                car_dis += distance[loc_index, 0]
                car_s.append(car_dis)
                car_window[signal].append(0)
                time_car += distance[loc_index, 0] / self.car_v
                time.append(time_car)
                car_p.append(p)
                car_road[signal].append(0)
                car_time[signal].append(time_car)
                car_un[signal].append(0)
                car_distance[signal].append(car_dis)

        # 计算总成本
        Z = sum(car_s) + sum(car_p)
        return Z, [road, car_demand, car_code, window_low], [car_road, car_distance, car_window, car_time, car_un], [
            car_s, car_p]


    def draw(self,Z,car_road,car_s,car_p):
         for i in range(len(car_road)):
              x=[location_xy[j][0] for j in car_road[i]]
              y=[location_xy[j][1] for j in car_road[i]]
              plt.scatter(x,y,c="red")
              if(i<len(car_road)-1):
                   plt.plot(x,y,label='第%.0f辆车的成本是：%.2f'% (i+1,car_s[i]+car_p[i]))
              else:
                   plt.plot(x,y,label='第%.0f辆车的成本是：%.2f\n%.0f辆车的总成本是：%.2f'%(i+1,car_s[i]+car_p[i],i+1,Z))
              for k in range(len(car_road[i])):
                   plt.annotate(car_road[i][k],xy=(x[k],y[k]),xytext=(x[k]+0.5,y[k]-0.5))
              plt.legend(prop={'family' : ['STSong'],'size' : 16})    #标签字体大小可修改
              font1={'weight':'bold','size':22}     #汉字大小可修改
              plt.xlabel("横坐标",font1)
              plt.title("最优配送方案线路图",font1)
              plt.ylabel("纵坐标",font1)
              plt.axis([0,120,0,110])
         plt.show()
    def save(self,road,result,file):             #保存编码以及各辆车的运行信息
         Z,save_total1,save_total2,save_total3=self.decode(road)
         wb=xlsxwriter.Workbook(file)
         ws=wb.add_worksheet('结果')
         colTitle1=['路径；','需求量：','车辆：','车辆数：','总成本：']
         colTitle2 = ['路径；', '路程：', '时间窗：', '时间：', '违约情况：']
         colTitle3 = ['距离成本；', '惩罚成本：', '总成本：']

         for i in range(4):
              ws.write(i,0,colTitle1[i])
              if(i<3):
                   for j in range(len(save_total1[i])):
                        if(i<2):
                             ws.write(i,j+1,save_total1[i][j])
                        else:
                             ws.write(i,j+1,save_total1[i][j]+1)
              else:
                   ws.write(i,1,len(save_total2[0]));ws.write(i,2,colTitle1[-1]);ws.write(i,3,Z)
         signal=4
         for i in range(len(save_total2[0])):
              ws.write(signal,0,'车辆：')
              ws.write(signal,1,i+1)
              signal+=1
              for j in range(len(colTitle2)):
                  sig=colTitle2[j]
                  ws.write(signal,1,sig)
                  for k in range(len(save_total2[j][i])):
                       if(j==2):
                            save_total2[j][i][k]=str(save_total2[j][i][k])
                       ws.write(signal,k+2,save_total2[j][i][k])
                  signal+=1
         for m in range(3):
              sig=colTitle3[m]
              ws.write(signal,2*m+1,sig)
              if(m<2):
                  ws.write(signal,2*m+2,save_total3[m][i])
              else:
                  ws.write(signal,2*m+2,save_total3[m-2][i]+save_total3[m-1][i])
         signal+=1
         ws=wb.add_worksheet('成本变化')
         ws.write_row('A1',['迭代次数','成本'])
         for c in range(len(result)):
            for r in range (len(result[c])):
             ws.write(c+1,r,result[c][r])
         wb.close()


if __name__ == '__main__':
    load_max=200             #载重
    car_v=2                  #速度
    parm_p=[200,400,0.3]       #惩罚成本各个参数
    xx_tool = tool(load_max, car_v, parm_p)

    yy = xx_tool.decode(np.array([ 23,  99,  78,  37,  11,  51,  89,  27,  36,  74,  87,  38,  35,  48,
  97,  83,  72,  84,  57,  93,  94,  19,  41,  10,  60,  26,  77,  56,
  58,  76,  32,  18,  54,  30,  42,  59,  91,   1,  69,  17,  65,  46,
  73,  55,  71,  67,   4,  13,  40,  25,  64,  29,  68,  45,  12,  92,
  33,  85,  61,  81,  80,  24,  79,   5,  34,  62,  95,  47,   8,  31,
  86,  98,  15,  43,  88,   3,  28,   2,  70,  39,  50,  96,  82,  63,
  75,   6,  66,  16,  20,   9,  22, 100,  44,  49,  53,   7,  14,  52,
  21,  90]))

    print(*yy)
