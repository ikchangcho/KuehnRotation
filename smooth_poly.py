import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from csv_to_plots import *
w = 5000
def smooth_poly(xy_list, half_window=w, poly_order=2, save_csv_filename=None):
    smooth_xy_list = []
    for idx, xy in enumerate(xy_list):
        xy = xy.astype(float)
        x = xy[:, 0]
        y = xy[:, 1]
        for i in range(len(y)):
            start = max(0, i - half_window)
            end = min(len(y), i + half_window + 1)
            p = np.polyfit(x[start:end], y[start:end], poly_order)
            y[i] = np.polyval(p, x[i])
        smooth_xy_list.append(np.vstack((x, y)).T)

        if save_csv_filename is not None:
            df = pd.DataFrame({'x': x, 'y': y})
            df.to_csv(f'{save_csv_filename}_w{half_window}_{idx}.csv', index=False)  # Save to CSV
    return smooth_xy_list

def cubic_spline_derivatives(xy_list):
    derivatives_list = []
    for idx, xy in enumerate(xy_list):
        # Ensure the data is of type float
        xy = xy.astype(float)
        x = xy[:, 0]
        y = xy[:, 1]

        # Create the cubic spline interpolator
        cs = CubicSpline(x, y)

        # Compute the first derivative
        dydx = cs(x, 1)  # The '1' here specifies the first derivative

        derivatives_list.append(np.vstack((x, dydx)).T)

        # # Optionally save the derivatives to a CSV
        # df = pd.DataFrame({'x': x, 'dydx': dydx})
        # df.to_csv(f'cubic_spline_derivatives_{idx}.csv', index=False)

    return derivatives_list

if __name__ == '__main__':
    filename_pattern = 'co2_per_gram_1cm2cm_*.csv'
    xy_list = load_csv(filename_pattern, indices=[4])

    xy_list[0] = xy_list[0][:, :]
    y = xy_list[0][:, 1]
    smooth_xy_list = smooth_poly(xy_list)
    smooth_y = smooth_xy_list[0][:, 1]
    smooth_xy_list2 = smooth_xy_list
    smooth_y2 = smooth_xy_list2[0][:, 1]

    # derv = cubic_spline_derivatives(xy_list)
    # dydx = derv[0][:, 1]
    # derv1 = cubic_spline_derivatives(smooth_xy_list)
    # dydx1 = derv1[0][:, 1]
    w2 = 3000
    derv2 = smooth_derivatives(smooth_xy_list2, half_window=w2)
    dydx2 = derv2[0][:, 1]

    fig, axs = plt.subplots(2, 1, figsize=(5, 7))
    start = 1000
    end = 1200
    axs[0].plot(y, label='Original')
    axs[0].plot(smooth_y, label='Smoothed')
    axs[0].plot(smooth_y2, label='Smoothed Five times')
    axs[0].set_title(f'[CO2], Five times smoothing (w={w})')
    axs[0].legend()
    #axs[1].plot(dydx)
    #axs[1].plot(dydx1)
    axs[1].plot(dydx2, color='g')
    axs[1].set_title(f'd[CO2]/dt, Poly derivatives (w={w2})')
    fig.suptitle('2cm Stack')

    plt.show()
