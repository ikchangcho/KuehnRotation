import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("280524_soillong_0.csv", delimiter=",")
time = data[:, 2] - data[0, 2]
co2 = data[:, 3] - data[0, 3]
hours = time / 3600

coefficients = np.polyfit(hours, co2, 1)
polynomial = np.poly1d(coefficients)
polyfit = polynomial(hours)

fig, ax = plt.subplots(1, 1)
ax.plot(hours, co2)
ax.plot(hours, polyfit, label=f'slope = {coefficients[0]:.2f}')
ax.set_xlabel('Time (hr)')
ax.set_ylabel(r'$CO_2$ (ppm)')
ax.set_title(r'Respiration of 0.85 g Soil Sample')
ax.legend()

plt.show()