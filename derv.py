import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

def smooth_derivative(x, y, w, p):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    #x_ext = np.concatenate((2*x[0] - x[w:0:-1], x, 2*x[-1] - x[-2:-w-2:-1]))
    #y_ext = np.concatenate((y[w:0:-1], y, y[-2:-w-2:-1]))
    derivatives = np.zeros(len(y))

    for i in range(len(y)):
        start = max(0, i - w)
        end = min(len(y), i + w + 1)
        derivatives[i] = Polynomial.fit(x[start:end], y[start:end], p).deriv()(x[i])

    return derivatives

# Directory containing the CSV files
directory = '.'

# Initialize an empty dictionary to store the numpy arrays
data_arrays1 = {}
data_arrays2 = {}

# Loop through the files in the directory
for file_name in os.listdir(directory):
    if file_name.startswith('260624_1cm2cm_') and file_name.endswith('.csv'):
        # Extract the file number from the file name
        file_number = file_name.split('_')[-1].split('.')[0]

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(directory, file_name))

        # Convert the DataFrame to a numpy array and store it in the dictionary
        data_arrays1[f'data{file_number}'] = df.values

for file_name in os.listdir(directory):
    if file_name.startswith('260624_3cm4cm_') and file_name.endswith('.csv'):
        # Extract the file number from the file name
        file_number = file_name.split('_')[-1].split('.')[0]

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(directory, file_name))

        # Convert the DataFrame to a numpy array and store it in the dictionary
        data_arrays2[f'data{file_number}'] = df.values

colors1 = ['k', 'r', 'g', 'b', 'r', 'g', 'b']
colors2 = ['k', 'r', 'g', 'b', 'r', 'g', 'b']
labels1 = ['Air', '7.59g', '5.30g', '6.53g', '16.54g', '20.17g', '20.03g']
labels2 = ['Air', '33.9g', '31.67g', '31.18g', '45.08g', '42.65g', '46.93g']
mass1 = [1, 7.97, 5.30, 6.53, 16.54, 20.17, 20.03]
mass2 = [1, 33.9, 31.67, 31.18, 45.08, 42.65, 46.93]
linewidths = [1, 1, 1, 1, 1, 1, 1]

init = 0
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

w = 3000
p = 2

for i, (color, label, linewidth, mass) in enumerate(zip(colors1, labels1, linewidths, mass1)):
    if i > 3 or i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays1[f'data{i}'][init:, 2] - data_arrays1[f'data{i}'][0, 2]) / 3600
    co2per_mass = (data_arrays1[f'data{i}'][init:, 3] - data_arrays1[f'data{i}'][init, 3]) / mass
    derv = smooth_derivative(hours, co2per_mass, w, p)
    ax1.plot(hours, derv, color=color, linewidth=linewidth, label=label)

for i, (color, label, linewidth, mass) in enumerate(zip(colors1, labels1, linewidths, mass1)):
    if i <= 3 or i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays1[f'data{i}'][init:, 2] - data_arrays1[f'data{i}'][0, 2]) / 3600
    co2per_mass = (data_arrays1[f'data{i}'][init:, 3] - data_arrays1[f'data{i}'][init, 3]) / mass
    derv = smooth_derivative(hours, co2per_mass, w, p)
    ax2.plot(hours, derv, color=color, linewidth=linewidth, label=label)

for i, (color, label, linewidth, mass) in enumerate(zip(colors2, labels2, linewidths, mass2)):
    if i > 3 or i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays2[f'data{i}'][init:, 2] - data_arrays2[f'data{i}'][0, 2]) / 3600
    co2per_mass = (data_arrays2[f'data{i}'][init:, 3] - data_arrays2[f'data{i}'][init, 3]) / mass
    derv = smooth_derivative(hours, co2per_mass, w, p)
    ax3.plot(hours, derv, color=color, linewidth=linewidth, label=label)

for i, (color, label, linewidth, mass) in enumerate(zip(colors2, labels2, linewidths, mass2)):
    if i <= 3 or i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays2[f'data{i}'][init:, 2] - data_arrays2[f'data{i}'][0, 2]) / 3600
    co2per_mass = (data_arrays2[f'data{i}'][init:, 3] - data_arrays2[f'data{i}'][init, 3]) / mass
    derv = smooth_derivative(hours, co2per_mass, w, p)
    ax4.plot(hours, derv, color=color, linewidth=linewidth, label=label)

ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
ax1.set_title(r'1cm stack')
ax2.set_title(r'2cm stack')
ax3.set_title(r'3cm stack')
ax4.set_title(r'4cm stack')

fig.set_size_inches(10, 8)
fig.suptitle(r'$CO_2$ production per gram of soil', fontsize=20)
fig.text(0.5, 0.04, 'Time (hours)', ha='center', fontsize=15)
fig.text(0.04, 0.5, r'$\Delta CO_2$ (ppm)', va='center', rotation='vertical', fontsize=15)

plt.show()