import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to load data from CSV files matching the filename pattern
def load_data(filename_pattern, indices=None):
    files = sorted(glob.glob(filename_pattern))
    if indices is None:
        indices = range(len(files))
    data_list = []
    for idx in indices:
        if idx < len(files):
            data = pd.read_csv(files[idx]).values
            data_list.append(data)
        else:
            print(f"Index {idx} is out of range for available files.")
    return data_list


# Function to process data, extracting specified columns and calculating derivatives
def choose_x_y(data_list, init=0, x_col=0, x_factor=1, y_col=1, y_factor=1):
    x_y_values = []
    for idx, data in enumerate(data_list):
        x = data[init:, x_col] * x_factor # Specified column as x values
        y = data[init:, y_col] * y_factor # Specified column as y values
        x_y_values.append((x, y))
        df = pd.DataFrame({'x': x, 'y': y})
        df.to_csv(f'y_values_{idx}.csv', index=False)  # Save to CSV
    return x_y_values

def derivatives(x_y_values):
    derivatives = []
    for idx, (x, y) in enumerate(x_y_values):
        dydx = np.gradient(y, x)  # Calculate the derivative
        derivatives.append((x, dydx))
        df = pd.DataFrame({'x': x, 'dydx': dydx})
        df.to_csv(f'derivatives_{idx}.csv', index=False)  # Save to CSV
    return derivatives

def smooth_derivatives(x_y_values, half_window=10, poly_order=2):
    smooth_derivatives = []
    for idx, (x, y) in enumerate(x_y_values):
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        dydx = np.zeros(len(y))
        for i in range(len(y)):
            start = max(0, i - half_window)
            end = min(len(y), i + half_window + 1)
            # Fit polynomial and calculate the derivative at point x[i]
            p = np.polyfit(x[start:end], y[start:end], poly_order)
            dydx[i] = np.polyval(np.polyder(p), x[i])
        smooth_derivatives.append((x, dydx))
        df = pd.DataFrame({'x': x, 'dydx': dydx})
        df.to_csv(f'smooth_derv_w{half_window}_{idx}.csv', index=False)  # Save to CSV
    return smooth_derivatives

def plots_separate(data, indices=None, titles=None, xlabels=None, ylabels=None):
    if indices is None:
        indices = range(len(data))
    selected_data = [data[i] for i in indices]

    if titles is None:
        titles = [''] * len(selected_data)
    if xlabels is None:
        xlabels = [''] * len(selected_data)
    if ylabels is None:
        ylabels = [''] * len(selected_data)

    fig, axs = plt.subplots(len(selected_data), 1, figsize=(8, 6 * len(selected_data)))
    if len(selected_data) == 1:
        axs = [axs]  # Ensure axs is a list even if there's only one plot
    for idx, ((x, y), title, xlabel, ylabel) in enumerate(zip(selected_data, titles, xlabels, ylabels)):
        axs[idx].plot(x, y, label=f'Data {indices[idx]}')
        axs[idx].set_title(f'{title}')
        axs[idx].set_xlabel(f'{xlabel}')
        axs[idx].set_ylabel(f'{ylabel}')
        axs[idx].legend()
    plt.tight_layout()
    plt.show()
def plots_overlap(data, indices=None, title='', xlabel='', ylabel=''):
    if indices is None:
        indices = range(len(data))
    selected_data = [data[i] for i in indices]

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    for idx, (x, y) in enumerate(selected_data):
        ax.plot(x, y, label=f'Data {indices[idx]}')
    ax.set_title(f'{title}')
    ax.set_xlabel(f'{xlabel}')
    ax.set_ylabel(f'{ylabel}')
    ax.legend()
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    filename_pattern = "260624_3cm4cm_*.csv"
    data_list = load_data(filename_pattern)
    data = choose_x_y(data_list, x_col=2, y_col=3)
    #derv = smooth_derivatives(data)
    plots_overlap(data, indices=[1, 2, 3])