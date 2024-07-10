from csv_to_plots import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d

# Load your data
data_list = load_csv('co2_per_gram_1cm2cm_4.csv')
data = data_list[0]
time = data[:, 0]  # Adjust the column names accordingly
co2 = data[:, 1]  # Adjust the column names accordingly

# Interpolate data to a uniform grid
uniform_time = np.linspace(time.min(), time.max(), num=len(time))
interpolator = interp1d(time, co2, kind='linear')
uniform_co2 = interpolator(uniform_time)

# Apply Savitzky-Golay filter to smooth the data
num_iterations = 3
window_length = 1001  # Choose a suitable window length
polyorder = 2  # Choose a suitable polynomial order
smoothed_co2 = savgol_filter(uniform_co2, window_length, polyorder)
for _ in range(num_iterations):
    smoothed_co2 = savgol_filter(smoothed_co2, window_length, polyorder)

# Calculate the derivative of the smoothed data
dt = uniform_time[1] - uniform_time[0]  # Calculate the time interval
co2_derivative = savgol_filter(uniform_co2, window_length, polyorder, deriv=1)

# Plot the original and smoothed data
plt.figure(figsize=(10, 6))
plt.plot(time, co2, label='Original Data')
plt.plot(uniform_time, smoothed_co2, label='Smoothed Data')
plt.xlabel('Time (hours)')
plt.ylabel('ΔCO2 (ppm)')
plt.legend()
plt.show()

# Plot the derivative
plt.figure(figsize=(10, 6))
plt.plot(uniform_time, co2_derivative, label='Derivative of Smoothed Data')
plt.xlabel('Time (hours)')
plt.ylabel('d(ΔCO2)/dt (ppm/hour)')
plt.legend()
plt.show()

