class DisjointSet:

    def __init__(self, element_num=None):
        self._father = {}
        self._rank = {}
        # 初始化时每个元素单独成为一个集合
        if element_num is not None:
            for i in range(element_num):
                self.add(i)

    def add(self, x):
        # 添加新集合
        # 如果已经存在则跳过
        if x in self._father:
            return
        self._father[x] = x
        self._rank[x] = 0

    def _query(self, x):
        # 如果father[x] == x，说明x是树根
        if self._father[x] == x:
            return x
        self._father[x] = self._query(self._father[x])
        return self._father[x]

    def merge(self, x, y):
        if x not in self._father:
            self.add(x)
        if y not in self._father:
            self.add(y)
        # 查找到两个元素的树根
        x = self._query(x)
        y = self._query(y)
        # 如果相等，说明属于同一个集合
        if x == y:
            return
        # 否则将树深小的合并到树根大的上
        if self._rank[x] < self._rank[y]:
            self._father[x] = y
        else:
            self._father[y] = x
            # 如果树深相等，合并之后树深+1
            if self._rank[x] == self._rank[y]:
                self._rank[x] += 1

    # 判断是否属于同一个集合
    def same(self, x, y):
        return self._query(x) == self._query(y)


# 构造数据
edges = [[1, 2, 7], [2, 3, 8], [2, 4, 9], [1, 4, 5], [3, 5, 5], [2, 5, 7], [4, 5, 15], [4, 6, 6], [5, 6, 8], [6, 7, 11],
         [5, 7, 9]]

if __name__ == "__main__":
    disjoinset = DisjointSet(8)
    # 根据边长对边集排序
    edges = sorted(edges, key=lambda x: x[2])
    res = 0
    for u, v, w in edges:
        if disjoinset.same(u, v):
            continue
        disjoinset.merge(u, v)
        res += w
    print(res)