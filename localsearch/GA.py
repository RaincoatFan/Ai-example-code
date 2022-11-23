import random
import numpy as np


def log(i, a, b):
    print("epoch --> ",
          str(i + 1).rjust(5, " "), " max:",
          str(round(a, 4)).rjust(8, " "), "mean:",
          str(round(b, 4)).rjust(8, " "), "alpha:",
          str(round(a / b, 4)).rjust(8, " "))


class GeneSolve:
## 初始定义，后续引用GeneSolve类方法为（初始种群数，最大迭代数，交叉概率，变异概率，最大适应度/平均适应度(扰动率趋于平稳则越接近1越好））
    def __init__(self, pop_size, epoch, cross_prob, mutate_prob, alpha, print_batch=10):
        self.pop_size = pop_size
        self.epoch = epoch
        self.cross_prob = cross_prob
        self.mutate_prob = mutate_prob
        self.print_batch = print_batch
        self.alpha = alpha
        self.width = 11
        self.best = None

        # 产生初始种群
        self.genes = np.array(
            [''.join([random.choice(['0', '1']) for i in range(self.width)]) for j in range(self.pop_size)])

    def inter_cross(self):
        """对染色体进行交叉操作"""
        ready_index = list(range(self.pop_size))
        while len(ready_index) >= 2:
            d1 = random.choice(ready_index)
            ready_index.remove(d1)
            d2 = random.choice(ready_index)
            ready_index.remove(d2)
            if np.random.uniform(0, 1) <= self.cross_prob:
                loc = random.choice(range(1, self.width - 1))
                d1_a, d1_b = self.genes[d1][0:loc], self.genes[d1][loc:]
                d2_a, d2_b = self.genes[d2][0:loc], self.genes[d2][loc:]
                self.genes[d1] = d1_a + d2_b
                self.genes[d2] = d2_a + d1_b

    def mutate(self):
        """基因突变"""
        ready_index = list(range(self.pop_size))
        for i in ready_index:
            if np.random.uniform(0, 1) <= self.mutate_prob:
                loc = random.choice(range(0, self.width))
                t0 = list(self.genes[i])
                t0[loc] = str(1 - int(self.genes[i][loc]))
                self.genes[i] = ''.join(t0)

    def get_adjust(self):
        """计算适应度(只有在计算适应度的时候要反函数，其余过程全都是随机的二进制编码）"""
        x = self.get_decode()
        return x * np.sin(x) + 12

    def get_decode(self):
        """编码，从表现型到基因型的映射"""
        # 编码其中int(x,2)表示讲x换为二进制编码，12.55则为区间[0,12.55]的delta，2**11则为2^11 这里的11则是编码长度（也就是转换的精度）
        # 求解精度为10^-2，即将一个单位长度（这里是12.55划分成1255份）进行划分，由于2^10 = 1024 < 2^11 = 2048，于是编码长度选取为11
        return np.array([int(x,2) * 12.55 / (2 ** 12 - 1) for x in self.genes])

    def cycle_select(self):
        """通过轮盘赌来进行选择"""
        adjusts = self.get_adjust()
        if self.best is None or np.max(adjusts) > self.best[1]:
            self.best = self.genes[np.argmax(adjusts)], np.max(adjusts)
        p = adjusts / np.sum(adjusts)
        cu_p = []
        for i in range(self.pop_size):
            cu_p.append(np.sum(p[0:i]))
        cu_p = np.array(cu_p)
        r0 = np.random.uniform(0, 1, self.pop_size)
        sel = [max(list(np.where(r > cu_p)[0]) + [0]) for r in r0]
        # 保留最优的个体
        if np.max(adjusts[sel]) < self.best[1]:
            self.genes[sel[np.argmin(adjusts[sel])]] = self.best[0]
        self.genes = self.genes[sel]

    def evolve(self):
        """逐代演化"""
        for i in range(self.epoch):
            self.cycle_select()  #种群选取
            self.inter_cross()   #染色体交叉
            self.mutate()        #计算适应度
            a, b = np.max(gs.get_adjust()), np.mean(gs.get_adjust())
            if i % self.print_batch == self.print_batch - 1 or i == 0:
                log(i, a, b)
            if a / b < self.alpha:
                log(i, a, b)
                print("进化终止，算法已收敛！共进化 ", i + 1, " 代！")
                break
