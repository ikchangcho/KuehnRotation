import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to load data from CSV files matching the filename pattern
def load_csv(filename_pattern, indices=None):
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
def define_xy(data_list, init=0, x_col=0, x_factor=1, y_col=1, y_factor=1, filename=None):
    xy_list = []
    for idx, data in enumerate(data_list):
        x = data[init:, x_col] * x_factor
        y = data[init:, y_col] * y_factor
        xy_list.append(np.vstack((x, y)).T)
        if filename is None:
            filename = 'y_values'
        df = pd.DataFrame({'x': x, 'y': y})
        df.to_csv(f'{filename}_{idx}.csv', index=False)  # Save to CSV
    return xy_list


def derivatives(xy_list):
    derivatives = []
    for idx, xy in enumerate(xy_list):
        x = xy[:, 0]
        y = xy[:, 1]
        dydx = np.gradient(y, x)  # Calculate the derivative
        derivatives.append((x, dydx))
        df = pd.DataFrame({'x': x, 'dydx': dydx})
        df.to_csv(f'derivatives_{idx}.csv', index=False)  # Save to CSV
    return derivatives


def smooth_derivatives(xy_list, half_window=10, poly_order=2):
    smooth_derivatives = []
    for idx, xy in enumerate(xy_list):
        x = xy[:, 0]
        y = xy[:, 1]
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


def plots_seperate(filename_pattern, indices=None, titles=None, xlabels=None, ylabels=None):
    data_list = load_csv(filename_pattern)

    if indices is None:
        indices = range(len(data_list))
    selected_data = [data_list[i] for i in indices]

    if titles is None:
        titles = [''] * len(selected_data)
    if xlabels is None:
        xlabels = [''] * len(selected_data)
    if ylabels is None:
        ylabels = [''] * len(selected_data)

    fig, axs = plt.subplots(len(selected_data), 1, figsize=(8, 6 * len(selected_data)))
    if len(selected_data) == 1:
        axs = [axs]  # Ensure axs is a list even if there's only one plot
    for idx, (data, title, xlabel, ylabel) in enumerate(zip(selected_data, titles, xlabels, ylabels)):
        x = data[:, 0]  # assuming x values are in the first column
        y = data[:, 1]  # assuming y values are in the second column
        axs[idx].plot(x, y, label=f'Data {indices[idx]}')
        axs[idx].set_title(f'{title}')
        axs[idx].set_xlabel(f'{xlabel}')
        axs[idx].set_ylabel(f'{ylabel}')
        axs[idx].legend()
    plt.tight_layout()
    plt.show()


def plots_overlap(filename_pattern, indices=None, title='', xlabel='', ylabel=''):
    data_list = load_csv(filename_pattern)

    if indices is None:
        indices = range(len(data_list))
    selected_data = [data_list[i] for i in indices]

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    for idx, data in enumerate(selected_data):
        x = data[:, 0]  # assuming x values are in the first column
        y = data[:, 1]  # assuming y values are in the second column
        ax.plot(x, y, label=f'Data {indices[idx]}')
    ax.set_title(f'{title}')
    ax.set_xlabel(f'{xlabel}')
    ax.set_ylabel(f'{ylabel}')
    ax.legend()
    plt.tight_layout()
    plt.show()


def std_over_sensors():
    filename_pattern = "020724_P*_calibrate_*.csv"
    data_list = load_csv(filename_pattern)
    xy_list = define_xy(data_list, x_col=2, x_factor=1 / 3600, y_col=3, filename='050724_CO2')
    xy_list_truncated = []
    for xy in xy_list:
        xy_truncated = xy[xy[:, 0] >= xy[0, 0] + 19]
        xy_truncated[:, 0] = xy_truncated[:, 0] - xy_truncated[0, 0]
        xy_list_truncated.append(xy_truncated)

    times = np.arange(1.5, 44.7, 0.1)
    dt = 1.5
    avg_CO2_at_time_points = np.zeros((len(times), 19))
    for j, xy in enumerate(xy_list_truncated):
        x = xy[:, 0]
        y = xy[:, 1]
        for i, t0 in enumerate(times):
            mask = (x > t0 - dt) & (x < t0 + dt)
            avg_CO2_at_time_points[i, j] = np.average(y[mask])
    variance = np.std(avg_CO2_at_time_points, axis=1)
    np.savetxt('050724_avg_CO2_at_time_points.csv', avg_CO2_at_time_points, delimiter=",",
               header=f'Average CO2 over dt = {dt} hour time span at every time point with interval 0.1 hour')
    np.savetxt('050724_std.csv', variance, delimiter=",",
               header='Standard deviation over 19 sensors at every time point with interval 0.1 hour')
    plt.plot(times, variance)
    plt.xlabel('Time after calibration (hours)')
    plt.ylabel(r'$\Delta CO_2$ (ppm)')
    plt.title(r'Standard deviation on $CO_2$ measurement over 19 sensors')
    plt.show()

# Example usage
if __name__ == "__main__":
    std_over_sensors()