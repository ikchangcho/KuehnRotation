from csv_to_plots import *

filename_pattern = "020724_P*_calibrate_*.csv"
data_list = load_csv(filename_pattern)
xy_list = define_xy(data_list, x_col=2, x_factor=1/3600, y_col=3)
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
for xy in xy_list:
    xy[:, 0] = xy[:, 0] - xy[0, 0]
    ax.plot(xy[:, 0], xy[:, 1], linewidth=0.1)
ax.set_title(r'19 Sensors Calibration')
ax.set_xlabel(r'Time (hour)')
ax.set_ylabel(r'$CO_2$ (ppm)')
plt.tight_layout()
plt.show()
