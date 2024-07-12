from csv_to_plots import *

filename_pattern1 = 'co2_per_gram_1cm2cm_*.csv'
smooth_xy_list = smooth_poly(smooth_poly(smooth_poly(load_csv(filename_pattern1))))
derv_list1 = smooth_derivatives(smooth_xy_list, save_csv_filename='smooth_derv_per_gram_1cm2cm')

filename_pattern2 = 'co2_per_gram_3cm4cm_*.csv'
smooth_xy_list = smooth_poly(smooth_poly(smooth_poly(load_csv(filename_pattern2))))
derv_list2 = smooth_derivatives(smooth_xy_list, save_csv_filename='smooth_derv_per_gram_3cm4cm')

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
for data in derv_list1[1:4]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[0, 0].plot(x, y)
axs[0, 0].set_title(f'1cm stack')
axs[0, 0].set_ylim([0, 14.5])

for data in derv_list1[4:]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[0, 1].plot(x, y)
axs[0, 1].set_title(f'2cm stack')
axs[0, 1].set_ylim([0, 9.5])

for data in derv_list2[1:4]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[1, 0].plot(x, y)
axs[1, 0].set_title(f'3cm stack')
axs[1, 0].set_ylim([0, 8])

for data in derv_list2[4:]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[1, 1].plot(x, y)
axs[1, 1].set_title(f'4cm stack')
axs[1, 1].set_ylim([0, 7])

fig.suptitle(r'$\frac{d[CO_2]}{dt}$ per gram of soil', fontsize=25)
fig.text(0.5, 0.04, 'Time (hour)', ha='center', fontsize=20)
fig.text(0.04, 0.5, r'$\frac{d[CO_2]}{dt}$ (ppm/hour)', va='center', rotation='vertical', fontsize=20)
fig.savefig('110724_derivatives_CO2_per_gram.png')
plt.show()