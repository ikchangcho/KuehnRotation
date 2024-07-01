import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing the CSV files
directory = '.'

# Initialize an empty dictionary to store the numpy arrays
data_arrays = {}

# Loop through the files in the directory
for file_name in os.listdir(directory):
    if file_name.startswith('250624_waterspike_') and file_name.endswith('.csv'):
        # Extract the file number from the file name
        file_number = file_name.split('_')[-1].split('.')[0]

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(directory, file_name))

        # Convert the DataFrame to a numpy array and store it in the dictionary
        data_arrays[f'data{file_number}'] = df.values

colors = ['k', 'r', 'r', 'r', 'b', 'b', 'b']
labels = ['Air', 'Soil First', 'Soil First', 'Soil First', 'Water First', 'Water First', 'Water First']
linestyles = ['-', ':', '-.', '-', ':', '-.', '-']
linewidths = [1, 0.5, 1, 1.5, 0.5, 1, 1.5]

init = 1000
fig, ax = plt.subplots(1, 1)
for i, (color, label, linestyle, linewidth) in enumerate(zip(colors, labels, linestyles, linewidths)):
    if i == 0:
        continue  # Skip the first iteration
    hours = (data_arrays[f'data{i}'][init:, 2] - data_arrays[f'data{i}'][0, 2]) / 3600
    co2 = data_arrays[f'data{i}'][init:, 3] - data_arrays[f'data{i}'][init, 3]

    # Ensure hours and co2 are of type float
    hours = hours.astype(float)
    co2 = co2.astype(float)

    coefficients = np.polyfit(hours, co2, 3)
    polynomial = np.poly1d(coefficients)

    # Calculate the derivative of the polynomial
    derivative = np.polyder(polynomial)
    polyfit_derivative = derivative(hours)

    ax.plot(hours, polyfit_derivative, color=color, linestyle=linestyle, linewidth=linewidth,
            label=label + ' Derivative')

# To avoid duplicate labels in the legend
handles, labels = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))
ax.legend(unique_labels.values(), unique_labels.keys())
ax.set_xlabel('Time (hours)')
ax.set_ylabel(r'$\Delta CO_2$ Derivative (ppm/hour)')
ax.set_title('Derivative of CO2 Concentration Over Time')
ax.set_ylim([0, 200])

plt.show()