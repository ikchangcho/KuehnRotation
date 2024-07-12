from csv_to_plots import *

filename_pattern1 = 'co2_per_gram_1cm2cm_*.csv'
data_list1 = load_csv(filename_pattern1)

filename_pattern2 = 'co2_per_gram_3cm4cm_*.csv'
data_list2 = load_csv(filename_pattern2)

fig, axs = plt.subplots(2, 2, figsize=(11, 8))
for data in data_list1[1:4]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[0, 0].plot(x, y)
axs[0, 0].set_title(f'1cm stack')

for data in data_list1[4:]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[0, 1].plot(x, y)
axs[0, 1].set_title(f'2cm stack')

for data in data_list2[1:4]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[1, 0].plot(x, y)
axs[1, 0].set_title(f'3cm stack')

for data in data_list2[4:]:
    x = data[:, 0]  # assuming x values are in the first column
    y = data[:, 1]  # assuming y values are in the second column
    axs[1, 1].plot(x, y)
axs[1, 1].set_title(f'4cm stack')

fig.suptitle(r'$[CO_2]$ per gram of soil', fontsize=20)
fig.text(0.5, 0.04, 'Time (hour)', ha='center', fontsize=15)
fig.text(0.04, 0.5, r'$\Delta CO_2$ (ppm)', va='center', rotation='vertical', fontsize=15)
fig.savefig('110724_CO2_per_gram.png')
plt.show()