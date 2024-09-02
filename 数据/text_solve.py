import  numpy as np
import  xlsxwriter

class data():
    def read(self):  #读取txt数据
        with open('./RC108.txt', encoding='utf-8') as f:
          f1=f.readlines()
          c,count=[],0
          for line in f1:
            t1=line.strip('\n')
            if (count>0):
                cc=[]
                signal = 0
                for j in  range(len(t1)):
                    if(t1[j]!=' '):
                         signal+=1
                    if(t1[j]== ' '):
                         signal=0
                    if (t1[j] == '.'):
                          cc.append(int(t1[j-signal:j]))
                c.append(cc)
            count+=1
        return  c
    def distance_caculate(self):  #计算两点距离
        c=self.read()
        if not  c:
            return np.array([]),np.array([])

        w = np.array(c)[:, :-1]
        print("w shape:", w.shape)
        print("w content:", w)

        if w.shape[0] == 0 or w.shape[1] < 2:
            return np.array([]), np.array([])

        Distance=np.zeros((w.shape[0],w.shape[0]))
        for i in  range(w.shape[0]-1):
            for j in range(i+1,w.shape[0]):
                dis=np.sqrt((w[j][0]-w[i][0])**2+(w[j][1]-w[i][1])**2)
                Distance[i,j]=dis
                Distance[j,i]=dis
        return  Distance,w
    def save(self):   #保存坐标信息与距离矩阵
        Distance,w=self.distance_caculate()
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