# A-star searching method
from copy import deepcopy as dp
import time

a = [[1, 3, 4],
     [2, 6, 0],
     [7, 5, 8]]
b = [[3, 0, 2],
     [6, 1, 5],
     [8, 7, 4]]

class AStar:
    def __init__(self, S0, G):
        self.S0 = S0
        self.G = G
        self.max_row = len(S0)
        self.max_col = len(S0[0])
        self.gn = 0
        self.nodes = 0
        self.close_list = {'Sn': [S0],
                           'gn': [0],
                           'hn': [self.get_h(S0)],
                           'fn': [self.get_h(S0)]}
        self.open_list = {'Sn': [], 'gn': [], 'hn': [], 'fn': []}

    def run(self):
        Sn = self.S0
        start = time.clock()
        while self.close_list['hn'][-1]:
            Sn = self.move(Sn)
            self.nodes += 1
        elapsed = time.clock() - start
        print(f'步数: {self.gn}, 访问节点数: {self.nodes}, 耗时: {elapsed}')
        return self.close_list

    def move(self, Sn):
        # restore gn
        self.gn = self.close_list['gn'][-1]
        self.gn += 1
        row_0, col_0 = self.get_loc(Sn, 0)
        # up
        if row_0 > 1:
            temp_n = Sn[row_0 - 2][col_0 - 1]
            temp_s = dp(Sn)
            temp_s[row_0 - 2][col_0 - 1] = 0
            temp_s[row_0 - 1][col_0 - 1] = temp_n
            self.add_open_list(temp_s)
        # down
        if row_0 < self.max_row:
            temp_n = Sn[row_0][col_0 - 1]
            temp_s = dp(Sn)
            temp_s[row_0][col_0 - 1] = 0
            temp_s[row_0 - 1][col_0 - 1] = temp_n
            self.add_open_list(temp_s)
        # left
        if col_0 > 1:
            temp_n = Sn[row_0 - 1][col_0 - 2]
            temp_s = dp(Sn)
            temp_s[row_0 - 1][col_0 - 2] = 0
            temp_s[row_0 - 1][col_0 - 1] = temp_n
            self.add_open_list(temp_s)
        # right
        if col_0 < self.max_col:
            temp_n = Sn[row_0 - 1][col_0]
            temp_s = dp(Sn)
            temp_s[row_0 - 1][col_0] = 0
            temp_s[row_0 - 1][col_0 - 1] = temp_n
            self.add_open_list(temp_s)
        # get best move
        fns = self.open_list['fn']
        best_idx = fns.index(min(fns))
        new_s = self.open_list['Sn'][best_idx]
        # update list
        self.close_list['Sn'].append(new_s)
        self.close_list['gn'].append(self.open_list['gn'][best_idx])
        self.close_list['hn'].append(self.open_list['hn'][best_idx])
        self.close_list['fn'].append(fns[best_idx])
        for key in self.open_list.keys():
            self.open_list[key].pop(best_idx)
        return new_s

    def add_open_list(self, temp_s):
        if temp_s in self.close_list['Sn']:
            return 0
        else:
            self.open_list['Sn'].append(temp_s)
            self.open_list['gn'].append(self.gn)
            self.open_list['hn'].append(self.get_h(temp_s))
            self.open_list['fn'].append(self.gn + self.get_h(temp_s))

    def get_h(self, Sn):
        h = 0
        for i in Sn:
            for j in i:
                if not j:
                    continue
                temp = j
                row_n, col_n = self.get_loc(Sn, temp)
                row_g, col_g = self.get_loc(self.G, temp)
                h = h + abs(row_n - row_g) + abs(col_n - col_g)
        return h

    @staticmethod
    def get_loc(array, num):
        for i in array:
            for j in i:
                if j == num:
                    row = array.index(i) + 1
                    col = i.index(j) + 1
                    return row, col
        return None

if __name__ == '__main__':
    method = AStar(a, b)
    method.run()
