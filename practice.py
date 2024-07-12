import numpy as np
import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8,9,10]
print(x[0:3])

fig, axs = plt.subplots(2, 2, figsize=(12,10))
fig.suptitle(r'$\frac{d[CO_2]}{dt}$ per gram of soil', fontsize=25)
fig.text(0.5, 0.04, 'Time (hour)', ha='center', fontsize=20)
fig.text(0.04, 0.5, r'$\Delta CO_2$ (ppm)', va='center', rotation='vertical', fontsize=20)
plt.show()