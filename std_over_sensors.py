from csv_to_plots import *

filename_pattern = "020724_P*_calibrate_*.csv"
data_list = load_csv(filename_pattern)
xy_list = define_xy(data_list, x_col=2, x_factor=1/3600, y_col=3)
xy_list_truncated = []
max_times = np.zeros(19)
for idx, xy in enumerate(xy_list):
    xy_truncated = xy[xy[:, 0] >= xy[0, 0] + 19]
    xy_truncated[:, 0] = xy_truncated[:, 0] - xy_truncated[0, 0]
    max_times[idx] = np.max(xy_truncated[:, 0])
    xy_list_truncated.append(xy_truncated)

max_time = np.min(max_times)
times = np.arange(1.5, max_time - 1.4, 0.1)
dt = 1.5
avg_CO2_at_time_points = np.zeros((len(times), 19))
for j, xy in enumerate(xy_list_truncated):
    x = xy[:, 0]
    y = xy[:, 1]
    for i, t0 in enumerate(times):
        mask = (x > t0 - dt) & (x < t0 + dt)
        avg_CO2_at_time_points[i, j] = np.average(y[mask])
std = np.std(avg_CO2_at_time_points, axis=1)
np.savetxt('050724_avg_CO2_at_time_points.csv', avg_CO2_at_time_points, delimiter=",",
           header=f'Average CO2 over dt = {dt} hour time span at every time point with interval 0.1 hour')
np.savetxt('050724_std.csv', std, delimiter=",",
           header='Standard deviation over 19 sensors at every time point with interval 0.1 hour')
plt.plot(times, std)
plt.xlabel('Time after calibration (hour)')
plt.ylabel(r'$\sigma(CO_2)$ (ppm)')
plt.title(r'Standard deviation on $CO_2$ measurement over 19 sensors')
plt.savefig('080724_std_19_sensors.png')
plt.show()

