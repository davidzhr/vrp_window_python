from ga import ga_m
from road_decode import tool
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
    load_max=200             #载重
    car_v=2                  #速度
    parm_p=[200,400,0.3]       #惩罚成本各个参数
    customers=100                #100个需求点
    go=tool(load_max,car_v,parm_p)   #解码

    generation,popsize=200,100     #迭代次数+种群规模
    p1,p2,C_size=0.8,0.2,3         #交叉变异概率，锦标赛选择框大小

    start = time.perf_counter()
    to=ga_m(customers,generation,popsize,[p1,p2,C_size],go)
    result,road=to.GA()            #遗传算法迭代，第一数字1代表粒子群和遗传算法公用初始解
    end = time.perf_counter()
    t2=end-start
    print('花费时间：%.2fs'%(t2))

    file='./result_ga.xlsx'
    go.save(road,result,file)          #保存
    Z,save_total1,save_total2,save_total3=go.decode(road)
    car_road,car_s,car_p=save_total2[0],save_total3[0],save_total3[1]
    go.draw(Z,car_road,car_s,car_p)  #画图

    result=np.array(result).reshape(len(result),2)
    plt.plot(result[:,0],result[:,1])
    font1={'weight':'bold','size':22} #汉字大小可修改
    plt.xlabel("迭代次数",font1)
    plt.title("成本变化图",font1)
    plt.ylabel("成本",font1)
    # plt.legend(prop={'family':['STSong'],'size'  :16}) #标签字体大小可改变
    plt.show()