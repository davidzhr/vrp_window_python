import  numpy as np
import  random

class ga_m():
     def __init__(self,customers,generation,popsize,parm_ga,go):
          self.customers=customers                #需求点个数
          self.generation=generation           #迭代次数
          self.popsize=popsize                 #种群规模
          self.p1=parm_ga[0]
          self.p2=parm_ga[1]
          self.C_size=parm_ga[2]
          self.go=go
     def road_cross(self,chrom_L1,chrom_L2):   #路径编码的pox交叉
         # 随机选择一个索引位置
         index = np.random.randint(1, self.customers + 1, 1)[0]

         # 初始化两个子代路径编码
         C1, C2 = np.zeros((1, chrom_L1.shape[0])), np.zeros((1, chrom_L1.shape[0]))

         # 用于存储大于索引位置的路径编码
         sig, svg = [], []

         # 固定位置的路径编码不变
         for i in range(chrom_L1.shape[0]):
             if chrom_L1[i] <= index:
                 C1[0, i] = chrom_L1[i]
             else:
                 sig.append(chrom_L1[i])
             if chrom_L2[i] <= index:
                 C2[0, i] = chrom_L2[i]
             else:
                 svg.append(chrom_L2[i])

         # 为0的地方按顺序添加路径编码
         signal1, signal2 = 0, 0
         for i in range(chrom_L1.shape[0]):
             if C1[0, i] == 0:
                 C1[0, i] = svg[signal1]
                 signal1 += 1
             if C2[0, i] == 0:
                 C2[0, i] = sig[signal2]
                 signal2 += 1

         # 返回两个子代路径编码
         return C1[0], C2[0]

     def Road_vara(self, W1, W2):  # 路径逆序变异
         # 将输入的路径编码转换为numpy数组
         W1, W2 = np.array([W1]), np.array([W2])

         # 随机选择两个索引位置，用于路径逆序变异
         index1 = random.sample(range(self.customers), 2)
         index2 = random.sample(range(self.customers), 2)

         # 对索引进行排序，确保从小到大
         index1.sort()
         index2.sort()

         # 提取路径编码的子路径
         L1 = W1[:, index1[0]:index1[1] + 1]
         L2 = W2[:, index2[0]:index2[1] + 1]

         # 初始化存储变异后路径编码的数组
         W_all = np.zeros((2, W1.shape[1]))
         W_all[0], W_all[1] = W1[0], W2[0]

         # 对第一个路径编码进行逆序变异
         for i in range(L1.shape[1]):
             W_all[0, index1[0] + i] = L1[0, L1.shape[1] - 1 - i]  # 反向读取路径编码

         # 对第二个路径编码进行逆序变异
         for i in range(L2.shape[1]):
             W_all[1, index2[0] + i] = L2[0, L2.shape[1] - 1 - i]  # 反向读取路径编码

         # 返回变异后的路径编码
         return W_all[0], W_all[1]



     def GA(self):
        # 初始化种群路径编码矩阵
        Total_road = np.zeros((self.popsize, self.customers))
        Total_road1 = np.zeros((self.popsize, self.customers))
        answer = []  # 存储每个个体的成本
        result = []  # 存储每代的最小成本

        # 遗传算法迭代
        for gen in range(self.generation):
            if gen < 1:  # 初始化种群
                for i in range(self.popsize):
                    road = np.arange(1, self.customers + 1, 1)  # 生成路径编码
                    np.random.shuffle(road)  # 随机打乱路径编码
                    Total_road[i] = road
                    Z, _, _, _ = self.go.decode(road)  # 计算路径成本
                    answer.append(Z)
                result.append([gen, min(answer)])  # 记录初始种群的最小成本
                print('遗传算法初始的成本：%.2f' % (min(answer)))

            answer1 = []  # 存储子代的成本
            for i in range(0, self.popsize, 2):
                chrom_L1 = Total_road[i]
                chrom_L2 = Total_road[i + 1]
                if np.random.rand() < self.p1:  # 交叉操作
                    C1, C2 = self.road_cross(chrom_L1, chrom_L2)
                else:
                    C1, C2 = chrom_L1, chrom_L2
                if np.random.rand() < self.p2:  # 变异操作
                    road1, road2 = self.Road_vara(C1, C2)
                else:
                    road1, road2 = C1, C2

                Total_road1[i] = road1
                Total_road1[i + 1] = road2
                Z, _, _, _ = self.go.decode(road1)  # 计算子代路径成本
                answer1.append(Z)
                Z, _, _, _ = self.go.decode(road2)
                answer1.append(Z)

            T_Road = np.vstack((Total_road, Total_road1))  # 合并子代与父代
            T_answer = answer + answer1
            Z1 = min(T_answer)
            best_idx = T_answer.index(Z1)  # 找最小成本个体
            best_road = T_Road[best_idx]

            if gen < self.generation:
                for i in range(self.popsize):
                    cab = random.sample(range(self.popsize * 2), self.C_size)  # 锦标赛选择
                    index, Z = [], []
                    for j in range(self.C_size):
                        index.append(cab[j])
                        Z.append(T_answer[cab[j]])
                    min_Z = Z.index(min(Z))
                    min_idx = index[min_Z]
                    Total_road[i], answer[i] = T_Road[min_idx], T_answer[min_idx]  # 选出的个体用于下次遗传

            if Z1 < min(answer):
                idx = answer.index(min(answer))
                answer[idx] = Z1
                Total_road[idx] = best_road
            result.append([gen + 1, Z1])
            print('遗传算法第%.0f次迭代的成本：%.2f' % (gen + 1, min(answer)))

        return result, best_road