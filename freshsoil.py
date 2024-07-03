import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Directory containing the CSV files
directory = '.'

# Initialize an empty dictionary to store the numpy arrays
data_arrays1 = {}
data_arrays2 = {}

# Loop through the files in the directory
for file_name in os.listdir(directory):
    if file_name.startswith('010724_freshsoil10g') and file_name.endswith('.csv'):
        # Extract the file number from the file name
        file_number = file_name.split('_')[-1].split('.')[0]

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(directory, file_name))

        # Convert the DataFrame to a numpy array and store it in the dictionary
        data_arrays1[f'data{file_number}'] = df.values

labels = ['Air', '1', '2', '3', '4', '5', '6']

init = 0
fig, ax = plt.subplots(1, 1)
for i, label in enumerate(labels):
    if i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays1[f'data{i}'][init:, 2] - data_arrays1[f'data{i}'][0, 2]) / 3600
    co2per_mass = (data_arrays1[f'data{i}'][init:, 3] - data_arrays1[f'data{i}'][init, 3])
    ax.plot(hours, co2per_mass, label=label)

ax.legend()
ax.set_xlabel('Time (hours)')
ax.set_ylabel(r'$\Delta CO_2$ (ppm)')
ax.set_title(r'10g Fresh soil')

plt.show()