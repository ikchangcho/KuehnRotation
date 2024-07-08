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
def define_xy(data_list, init=0, x_col=0, x_factor=1, y_col=1, y_factor=1, save_csv_filename=None, diff=False):
    xy_list = []
    for idx, data in enumerate(data_list):
        if isinstance(x_factor, list):
            x = data[init:, x_col] * x_factor[idx]
        else:
            x = data[init:, x_col] * x_factor
        if isinstance(y_factor, list):
            y = data[init:, y_col] * y_factor[idx]
        else:
            y = data[init:, y_col] * y_factor
        if diff:
            x = x - x[0]
            y = y - y[0]
        xy_list.append(np.vstack((x, y)).T)

        if save_csv_filename is not None:
            df = pd.DataFrame({'x': x, 'y': y})
            df.to_csv(f'{save_csv_filename}_{idx}.csv', index=False)  # Save to CSV
    return xy_list


def derivatives(xy_list, save_csv=True):
    derivatives = []
    for idx, xy in enumerate(xy_list):
        x = xy[:, 0]
        y = xy[:, 1]
        dydx = np.gradient(y, x)  # Calculate the derivative
        derivatives.append(np.vstack((x, dydx)).T)
        if save_csv:
            df = pd.DataFrame({'x': x, 'dydx': dydx})
            df.to_csv(f'derivatives_{idx}.csv', index=False)  # Save to CSV
    return derivatives


def smooth_derivatives(xy_list, half_window=5000, poly_order=2, indices=None, save_csv_filename=None):
    smooth_derivatives = []
    if indices is None:
        indices = range(len(xy_list))
    xy_selected = [xy_list[i] for i in indices]

    for idx, xy in enumerate(xy_selected):
        xy = xy.astype(float)
        x = xy[:, 0]
        y = xy[:, 1]
        dydx = np.zeros(len(y))
        for i in range(len(y)):
            start = max(0, i - half_window)
            end = min(len(y), i + half_window + 1)
            # Fit polynomial and calculate the derivative at point x[i]
            p = np.polyfit(x[start:end], y[start:end], poly_order)
            dydx[i] = np.polyval(np.polyder(p), x[i])
        smooth_derivatives.append(np.vstack((x, dydx)).T)

        if save_csv_filename is not None:
            df = pd.DataFrame({'x': x, 'dydx': dydx})
            df.to_csv(f'{save_csv_filename}_w{half_window}_{idx}.csv', index=False)  # Save to CSV
    return smooth_derivatives


def csv_to_plots_seperate(filename_pattern, indices=None, titles=None, xlabels=None, ylabels=None):
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


def csv_to_plots_overlap(filename_pattern, indices=None, title='', xlabel='', ylabel='', legend=True, save_file_name=None):
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
    if legend is True:
        ax.legend()
    plt.tight_layout()
    if save_file_name is not None:
        fig.savefig(save_file_name)
    plt.show()


def list_to_plots_overlap(data_list, indices=None, title='', xlabel='', ylabel='', legend=True, save_file_name=None):
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
    if legend is True:
        ax.legend()
    plt.tight_layout()
    if save_file_name is not None:
        fig.savefig(save_file_name)
    plt.show()



# Example usage
if __name__ == "__main__":
    filename_pattern1 = '260624_1cm2cm_*.csv'
    data_list = load_csv(filename_pattern1)
    xy_list = define_xy(data_list, x_col=2, x_factor=1/3600, y_col=3, y_factor=[1, 1/7.97, 1/5.30, 1/6.53, 1/16.54, 1/20.17, 1/20.03],
                        diff=True, save_csv_filename='co2_per_gram_1cm2cm')
    derv_list = smooth_derivatives(xy_list, save_csv_filename='derv_per_gram_1cm2cm')
    list_to_plots_overlap(derv_list, xlabel='Time (hour)',
                         ylabel=r'$\frac{d (\Delta CO_2)}{dt}$ (ppm/hour)', indices=[1, 2, 3],
                         title=r'Time derivative of $\Delta CO_2$ per gram of soil' f'\n 1cm Stack', legend=False,
                         save_file_name='080724_derv_1cm.png')
    plt.close('all')
    list_to_plots_overlap(derv_list, xlabel='Time (hour)',
                         ylabel=r'$\frac{d (\Delta CO_2)}{dt}$ (ppm/hour)', indices=[4, 5, 6],
                         title=r'Time derivative of $\Delta CO_2$ per gram of soil' f'\n 2cm Stack', legend=False,
                         save_file_name='080724_derv_2cm.png')
    plt.close('all')

    filename_pattern2 = '260624_3cm4cm_*.csv'
    data_list = load_csv(filename_pattern2)
    xy_list = define_xy(data_list, x_col=2, x_factor=1/3600, y_col=3, y_factor=[1, 1/33.9, 1/31.67, 1/31.18, 1/45.08, 1/42.65, 1/46.93],
                        diff=True, save_csv_filename='co2_per_gram_3cm4cm')
    derv_list = smooth_derivatives(xy_list, save_csv_filename='derv_per_gram_3cm4cm')
    list_to_plots_overlap(derv_list, xlabel='Time (hour)',
                         ylabel=r'$\frac{d (\Delta CO_2)}{dt}$ (ppm/hour)', indices=[1, 2, 3],
                         title=r'Time derivative of $\Delta CO_2$ per gram of soil' f'\n 3cm Stack', legend=False,
                         save_file_name='080724_derv_3cm.png')
    plt.close('all')
    list_to_plots_overlap(derv_list, xlabel='Time (hour)',
                         ylabel=r'$\frac{d (\Delta CO_2)}{dt}$ (ppm/hour)', indices=[4, 5, 6],
                         title=r'Time derivative of $\Delta CO_2$ per gram of soil' f'\n 4cm Stack', legend=False,
                         save_file_name='080724_derv_4cm.png')
    plt.close('all')