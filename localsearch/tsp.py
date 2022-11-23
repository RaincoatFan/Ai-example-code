import random   #一个具有随机生成序列、数等功能的库
city = ['a', 'b', 'c', 'd', 'e']  #设置5个城市点
#生成的各点到其他所有点的段（例如：ab,ac,ad,ae......）
paragraph = []
for i in range(len(city)):    #for ? in ? range()  for循环基本格式
    for j in range(len(city)):
        # 利用if-else双分支选择结构。如果出现aa,bb等重复点的段则不添加到列表paragraph中，不重复则将段加入列表paragraph
        if city[i]==city[j]:
            continue    #跳出本次循环，进入下一个循环
        else:
            paragraph.append(city[i] + city[j])
#print(paragraph)  #输出生成的每一个段的列表
# random.sample(sequence, k) 从指定序列中随机获取指定长度的片断并随机排列,结果以列表的形式返回。利用它生成随机距离和随机起点
rout=random.sample(range(1,50), len(paragraph))  #根据列表paragraph中的元素随机生成距离
first = random.sample(city, 1)    #定义起点为first，随机生成
print(first)  #输出从city中随机选择的起点

second = []    #用于暂时存放遍历出的路径，该路径最后会加在first中
for i in range(len(city) - 1):
    for i in first:
        for j in city:
            if i[len(i)-1]!=j and j not in i:    #if单分支选择结构。用first中的元素作为起点通过遍历列表city中的元素寻找下一个要走的节点。
                first1=i+j   #i+j表示让原来已经走过的节点加上新走的路径变成一个新的字符串first1
                second.append(first1)
    first = second.copy()    #将列表second中的元素存入first中作为下一次循环的起点。
    second.clear()   #将second中的元素清空以便存放下一次循环产生的新的路径。
# print(first)    #本次输出为所有路径，最后没回到原点
for i in range(len(first)):  #通过查找first每个元素的第一个字母加上即可表示完整路径。
    first[i]+=first[i][0]
# print(first)    #本次输出为所有路径，回到原点
length=[]    #创建路程长度列表
road=[]     #创建路径列表
journey={}   #创建路径及其对应路程的字典
# 接下来遍历first中的元素，再根据下标确定路径中每两个连续的点对应在paragraph中的下标，road和paragraph的下标是对应的。
for i in first:
    journey1 = 0    #用于遍历路径计算总路程
    #for循环嵌套if-else双分支选择结构，判断段是否是ab,如果是ba的话就让它变成ab
    for j in range(len(i)-1):
        if ord(i[j])<ord(i[j+1]):
            r = i[j]+i[j+1]
        else:
            r = i[j+1]+i[j]
        journey1+=rout[paragraph.index(r)]   #将通过下标找到相应每两地的距离相加即可得到完整路径所走的总路程。
    length.append(journey1)  #append() 方法用于在列表末尾添加新的对象。即将总路程长加入到journey1中
    journey[i]=journey1    #将路径与对应的总路程长添加到字典journey中
print(journey)  #输出所有路径及其对应的路程
min1=length.index(min(length))   #利用min函数找最短路径及其对应路程长度，min代表最短长度，min1代表最短路径
print(first[min1],'是最短路径，路程长度为',min(length))   #输出找出的最短路径及其路程
