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


colors1 = ['k', 'r', 'r', 'r', 'b', 'b', 'b']
colors2 = ['k', 'g', 'g', 'g', 'm', 'm', 'm']
labels1 = ['Air', '1cm', '1cm', '1cm', '2cm', '2cm', '2cm']
labels2 = ['Air', '3cm', '3cm', '3cm', '4cm', '4cm', '4cm']
mass1 = [1, 7.97, 5.30, 6.53, 16.54, 20.17, 20.03]
mass2 = [1, 33.9, 31.67, 31.18, 45.08, 42.65, 46.93]
linewidths = [1, 0.5, 1, 1.5, 0.5, 1, 1.5]

init = 0
fig, ax = plt.subplots(1, 1)
for i, (color, label, linewidth, mass) in enumerate(zip(colors1, labels1, linewidths, mass1)):
    if i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays1[f'data{i}'][init:, 2] - data_arrays1[f'data{i}'][0, 2]) / 3600
    co2per_mass = (data_arrays1[f'data{i}'][init:, 3] - data_arrays1[f'data{i}'][init, 3]) / mass
    ax.plot(hours, co2per_mass, color=color, linewidth=linewidth, label=label)

for i, (color, label, linewidth, mass) in enumerate(zip(colors2, labels2, linewidths, mass2)):
    if i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays2[f'data{i}'][init:, 2] - data_arrays2[f'data{i}'][0, 2]) / 3600
    co2per_mass = (data_arrays2[f'data{i}'][init:, 3] - data_arrays2[f'data{i}'][init, 3]) / mass
    ax.plot(hours, co2per_mass, color=color, linewidth=linewidth, label=label)

# To avoid duplicate labels in the legend
handles, labels1 = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels1, handles))
ax.legend(unique_labels.values(), unique_labels.keys())
ax.set_xlabel('Time (hours)')
ax.set_ylabel(r'$\Delta CO_2$ (ppm)')
ax.set_title(r'$CO_2$ production per gram of soil')

plt.show()