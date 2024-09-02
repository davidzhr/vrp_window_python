import  numpy as np
import  xlsxwriter
np.set_printoptions(threshold=np.inf)

class data():
    def read(self):  #读取txt数据
        f=open('./RC108.txt', encoding='utf-8')
        f1=f.readlines()
        c,count=[],-1
        for line in f1:
            count += 1
            t1=line.strip('\n')
            if (count>0):
                cc=[]
                for i in t1.split():
                    cc.append(int(i))
                c.append(cc)
        return c

    def diatance_caculate(self):  #计算两点距离
        c=self.read()
        print(c)
        w=np.array(c)[:,:-1]
        Distance=np.zeros((w.shape[0],w.shape[0]))
        for i in  range(w.shape[0]-1):
            for j in range(i+1,w.shape[0],1):
                dis=np.sqrt((w[j][0]-w[i][0])**2+(w[j][1]-w[i][1])**2)
                Distance[i,j]=dis
                Distance[j,i]=dis
        return  Distance,w
    def save(self):   #保存坐标信息与距离矩阵
        Distance,w=self.diatance_caculate()
        print(Distance)
        # print(w)
        location_xy = list()
        demand = list()
        time_window = list()
        for i in w:
            location_xy.append([i[0], i[1]])
            demand.append(i[2])
            time_window.append([i[3], i[4]])

        print(location_xy)
        print(demand)
        print(time_window)

        with open('data_text.txt', 'w') as f:
            f.write(f'location_xy={location_xy}')
            f.write('\n')
            f.write(f'demand={demand}')
            f.write('\n')
            f.write(f'time_window={time_window}')
            f.write('\n')
            f.write(str(Distance.tolist()))




        total_save=[w,Distance]
        wb=xlsxwriter.Workbook('./data.xlsx')
        sheet=['坐标','距离']
        rowTitle=['x坐标','y坐标','需求量','时间窗开始时间','时间窗结束时间']
        for i in range(2):
            ws=wb.add_worksheet(sheet[i])
            if(i<1):
                ws.write_row('B1',rowTitle)
            for c in range(total_save[i].shape[0]):
                     for r in range(total_save[i].shape[1]):
                          ws.write(c+1,r+1,total_save[i][c,r])
        wb.close()
to=data()
to.save()