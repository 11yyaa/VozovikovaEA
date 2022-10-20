#file = open('data.txt', 'r')
#file.read()
#file.close()

import numpy as np
import matplotlib.pyplot as plt
with open('settings.txt', 'r') as settings:
    for line in settings.readlines():
        if (line != '\n'):
            tmp = tuple([item for item in line.split()])
            s_freq = float(tmp[2])
            step = float(tmp[5])
data_array = np.loadtxt("data.txt", dtype = float)
t = []
u = []
tdots = []
udots = []
count = 0

with open ("data.txt", 'r') as data:
    for line in data.readlines():
        if line != '\n':
            count += 1
            x, y = tuple ([float(item) for item in line.split()])
            print(x, y)
            t.append(x)
            u.append(y)
fig, ax = plt.subplots(figsize=(16,10), dpi=400)
print (t)
print (u)
ax.plot(t, u)
#plt.plot(, [0, 1, 2, 3, 3.3, 3.5])
plt.plot([0, 450], [0, 1, 2, 3, 3.3, 3.5])
plt.suptitle('График зависимости напряжения от времени на С')
plt.ylabel('Напряжение, В')
plt.xlabel('Время, с')
fig.savefig('vvv.png')
plt.show()