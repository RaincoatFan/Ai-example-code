import numpy as np
import matplotlib.pyplot as plt
import math


def function(x):
    return -(10 * math.sin(5 * x) + 7 * math.cos(4 * x))


initT = 1000
minT = 1
iterL = 1000
eta = 0.95
k = 1

x0 = 1.5  # 10*(2*np.random.rand()-1)

t = initT
print("init solution :", x0)
yy = []
xx = np.linspace(0, 10, 300)
for i in range(len(xx)):
    yy.append(function(xx[i]))
plt.figure()
plt.plot(xx, yy)
plt.plot(x0, function(x0), 'o')

x_old = x0
while t > minT:
    for i in range(iterL):  # MonteCarlo method reject propblity
        value_old = function(x_old)
        x_new = x_old + np.random.rand() - 0.5
        if x_new >= 0 and x_new <= 10:
            value_new = function(x_new)
            res = value_new - value_old
            if res < 0 or np.exp(-res / (k * t)) > np.random.rand():
                x_old = x_new
    t = t * eta

print("最优解: ", x_old)
print("最优值：", function(x_old))
plt.plot(x_old, function(x_old), 'or')
plt.show()