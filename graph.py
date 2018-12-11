import sys
import math
import numpy as np
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

input_file = sys.argv[1] #平均のやつ
with open(input_file) as f:
    data = f.read()
data = data.split("\n")
li = []
for info in data[1:]:
    tmp = info.replace(", ", ",").split(",")
    if tmp == ['']:
        continue
    li.append(tmp)

steps = []
nodes = []
times = []

for info in li:
    try:
        steps.append(int(info[0]))
        nodes.append(float(info[1]))
        times.append(float(info[2]))
    except Exception as e:
        print(info)
        raise e

#グラフ描画
# # plt.figure(figsize=(10,10))
# # plt.subplot(1,2,1)
# plt.plot(steps, nodes, color="r", marker="o")
# plt.title("step and nodes")
# plt.xlabel('step')
# plt.ylabel('average nodes')
# plt.legend()
# plt.show()
# plt.savefig(input_file.split(".")[0]+"_node.png")
# plt.figure()
# # plt.subplot(1,2,2)
# plt.plot(steps, times, color="b", marker="o")
# plt.title("step and time")
# plt.xlabel('step')
# plt.ylabel('time[ms]')
# # plt.legend()
# # plt.bar(steps, times)#, color="r", marker="o")
# # plt.title('')
# plt.show()
# plt.savefig(input_file.split(".")[0]+"_time.png")

#多項式関数近似
x = np.array(steps)
# y = np.array(nodes)
y = np.array(times)
d = 7
plt.scatter(x,y)
f = np.poly1d(np.polyfit(x,y,d))
print(f)
y = f(x)
plt.plot(x, y, label=f'd={d}')
plt.show()
"""=======
nodeはd=5????!!!
timeはd=5????!!!
"""

# max_num = 30
# # y = [n**10/1000 for n in range(1,max_num)]
# y = [n**3.5/140 for n in range(1,max_num)]
# # y = [n**10/370000000000 for n in range(1,max_num)] # times!!!
# # y = [n**10/45000000000 for n in range(1,max_num)] # nodes!!!
# y = [n**5/4500 for n in range(1,max_num)] # nodes!!!
# for i,ye in enumerate(y):
#     print(i+1, ye)

# yy = []
# for step in steps:
#     yy.append(y[step-1])

# # y = [math.factorial(n) for n in range(1,10)]
# plt.plot(steps, yy)
# plt.show()

# # for info in li:
# #     print(int(info[0]), math.log(float(info[1]), int(info[0])))