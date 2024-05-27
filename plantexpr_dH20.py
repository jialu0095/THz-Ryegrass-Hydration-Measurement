#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.chdir('plant_expr_API/all_plant_data')
# os.chdir('plant_expr_API')

#%%
# output: dH20(mm)
dH20_unit = 'mm'
def calculate_dH20_plant(I_ref, I_smp, dB_ref, dB_smp, group):
    I_ref = np.array(I_ref)
    I_smp = np.array(I_smp)
    dB_ref = np.array(dB_ref)
    dB_smp = np.array(dB_smp)

    # remove empty pixels
    zero_indices = np.where((I_ref == 0) | (I_smp == 0))[0]
    print('empty pixels: ', len(zero_indices))
    I_ref = np.delete(I_ref, zero_indices)
    I_smp = np.delete(I_smp, zero_indices)
    dB_ref = np.delete(dB_ref, zero_indices)
    dB_smp = np.delete(dB_smp, zero_indices)

    # if(group == 2):
    #     dB_smp -= 0.3

    # if(group == 5):
    #     dB_smp -= 0.3

    # get mean value
    I_mean_ref = np.mean(I_ref)
    I_mean_smp = np.mean(I_smp)
    dB_mean_ref = np.mean(dB_ref)
    dB_mean_smp = np.mean(dB_smp)

    print(f'dB_mean_smpl: {dB_mean_smp}')
    
    # calculate dH20
    # dH20 = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / 85 # cm
    dH20 = (np.log(I_mean_ref / I_mean_smp) + 0.1*np.log(10) * (dB_mean_ref - dB_mean_smp)) / 85 # cm
    dH20 *= 10 # cm to mm
    # mm to um
    if dH20_unit == 'um':
        dH20 *= 1000

    # remove -inf nan values
    valid_values_mean = np.nanmean(np.where(dH20 == -np.inf, np.nan, dH20))
    dH20 = np.where(np.isneginf(dH20) | np.isnan(dH20), valid_values_mean, dH20)

    return dH20

def print_mean_I0(I_group, group_name, dB_group, dB_name, times):
    for i in range(0,times):
        I = I_group[i]
        dB = dB_group[i]
        zero_indices = np.where(I == 0)[0]
        I = np.delete(I, zero_indices)
        dB = np.delete(dB, zero_indices)
        I_0 = 10**(dB/10)*I
        I_0_mean = np.mean(I_0)
        print(f'{group_name} day {i+1} mean I_0: ', I_0_mean)

def cal_mean_I0(I_group, group_name, dB_group, dB_name, times):
    I_0_means = []
    for i in range(0,times):
        I = I_group[i]
        dB = dB_group[i]
        zero_indices = np.where(I == 0)[0]
        I = np.delete(I, zero_indices)
        dB = np.delete(dB, zero_indices)
        I_0 = 10**(dB/10)*I
        I_0_mean = np.mean(I_0)
        I_0_means.append(I_0_mean)
    return I_0_means

def cal_RWC_THz(dH20, dH20_max):
    RWC_THz = dH20/dH20_max
    return RWC_THz

# load THz data from csv filess
# attenuation(dB), intensity(I)
def load_THz_data(species, plant_number, times):
    I = [[] for _ in range(times)]
    dB = [[] for _ in range(times)]
    for i in range(0,times):
        I[i] = np.loadtxt('I_wet' + str(i+1) + '_' + species + '_' + plant_number + '.csv', delimiter=' ', comments='#')
        dB[i] = np.loadtxt('dB_wet' + str(i+1) + '_' + species + '_' + plant_number + '.csv', delimiter=' ', comments='#')
    return I, dB

# calculate dH20 for all dry times
def cal_all_dH20(I, dB, times):
    dH20 = [[] for _ in range(times)]
    for i in range(0,times):
        dH20[i] = calculate_dH20_plant(I[-1], I[i], dB[-1], dB[i], i+1)
    return dH20

def plot_multiple_graphs(y_arrays, times, titles):
    """
    Create multiple charts in a single row of subplots.

    Parameters:
    - y_arrays : list of y-value arrays for each chart
    - times : current dry time, used to determine the range of the x-axis
    - titles : list of titles for each chart
    """
    n = len(y_arrays)   # number of charts
    fig, axs = plt.subplots(1, n, figsize=(6*n, 8))  # create n subplots in a row
    fig.suptitle('RWC_THz for Each Group')

    # if only one chart, axs is not a list
    if n == 1:
        axs = [axs]

    x_values = range(1, times + 1)
    
    for i in range(n):
        axs[i].plot(x_values, y_arrays[i], marker='o')
        axs[i].set_title(titles[i])
        axs[i].set_xlabel('Time[/20mins]')
        axs[i].set_ylabel('RWC_THz[%]')

    plt.tight_layout()
    plt.show()

# all in one functions
def THz_results(species, plant_number, times):
    I, dB = load_THz_data(species, plant_number, times)
    dH20 = cal_all_dH20(I, dB, times)
    RWC_THz = cal_RWC_THz(dH20, dH20[0])
    return RWC_THz
# %%
times = 13
RWC_THz_One50_3 = THz_results('One50', '3', times)
plot_multiple_graphs([RWC_THz_One50_3], times, ['One50-3'])
# Print RWC_THz_One50_3 vertically
for value in RWC_THz_One50_3:
    print(value)

#%%
# load THz data
I_One50_1 = [[] for _ in range(times)]
I_One50_2 = [[] for _ in range(times)]
# I_GA66_1 = [[] for _ in range(times)]
# I_GA66_2 = [[] for _ in range(times)]

dB_One50_1 = [[] for _ in range(times)]
dB_One50_2 = [[] for _ in range(times)]
# dB_GA66_1 = [[] for _ in range(times)]
# dB_GA66_2 = [[] for _ in range(times)]

for i in range(0,times):
    print(i)
    I_One50_1[i] = np.loadtxt('I_wet'+str(i+1)+'_One50_1.csv', delimiter=' ', comments='#')
    I_One50_2[i] = np.loadtxt('I_wet'+str(i+1)+'_One50_2.csv', delimiter=' ', comments='#')
    # I_GA66_1[i] = np.loadtxt('I_wet'+str(i+1)+'_GA66_1.csv', delimiter=' ', comments='#')
    # I_GA66_2[i] = np.loadtxt('I_wet'+str(i+1)+'_GA66_2.csv', delimiter=' ', comments='#')
    
    dB_One50_1[i] = np.loadtxt('dB_wet'+str(i+1)+'_One50_1.csv', delimiter=' ', comments='#')
    dB_One50_2[i] = np.loadtxt('dB_wet'+str(i+1)+'_One50_2.csv', delimiter=' ', comments='#')
    # dB_GA66_1[i] = np.loadtxt('dB_wet'+str(i+1)+'_GA66_1.csv', delimiter=' ', comments='#')
    # dB_GA66_2[i] = np.loadtxt('dB_wet'+str(i+1)+'_GA66_2.csv', delimiter=' ', comments='#')



#%%
# calculate dH20
dH20_One50_1 = [[] for _ in range(times)]
dH20_One50_2 = [[] for _ in range(times)]
# dH20_GA66_1 = [[] for _ in range(times)]
# dH20_GA66_2 = [[] for _ in range(times)]


for i in range(0,times):
    print(i)
    dH20_One50_1[i] = calculate_dH20_plant(I_One50_1[-1], I_One50_1[i], dB_One50_1[-1], dB_One50_1[i], i+1)
    dH20_One50_2[i] = calculate_dH20_plant(I_One50_2[-1], I_One50_2[i], dB_One50_2[-1], dB_One50_2[i], i+1)
    # dH20_GA66_1[i] = calculate_dH20_plant(I_GA66_1[-1], I_GA66_1[i], dB_GA66_1[-1], dB_GA66_1[i], i+1)
    # dH20_GA66_2[i] = calculate_dH20_plant(I_GA66_2[-1], I_GA66_2[i], dB_GA66_2[-1], dB_GA66_2[i], i+1)
    



#%%
print(dH20_One50_1)
print(dH20_One50_2) 
# print(dH20_GA66_1)
# print(dH20_GA66_2)

# RWC_THz_One50_1 = dH20_One50_1/dH20_One50_1[-1]
#%%


RWC_THz_One50_1 = cal_RWC_THz(dH20_One50_1, dH20_One50_1[0])
RWC_THz_One50_2 = cal_RWC_THz(dH20_One50_2, dH20_One50_2[0])
# RWC_THz_GA66_1 = cal_RWC_THz(dH20_GA66_1, dH20_GA66_1[0])
# RWC_THz_GA66_2 = cal_RWC_THz(dH20_GA66_2, dH20_GA66_2[0])
print(RWC_THz_One50_1)
print(RWC_THz_One50_2)
# print(RWC_THz_GA66_1)
# print(RWC_THz_GA66_2)

# Plotting RWC_THz for each group
fig, axs = plt.subplots(1, 2, figsize=(12, 8))
fig.suptitle('RWC_THz for Each Group')

axs[0].plot(range(1, times+1), RWC_THz_One50_1, marker='o')
axs[0].set_title('One50-1')
axs[0].set_xlabel('Day')
axs[0].set_ylabel('RWC_THz')

axs[1].plot(range(1, times+1), RWC_THz_One50_2, marker='o')
axs[1].set_title('One50-2')
axs[1].set_xlabel('Day')
axs[1].set_ylabel('RWC_THz')

plt.tight_layout()
plt.show()


# %%
# gravimetric data
RWC_gravimetric_One50_1 = [0.941810345,
                            0.638513514,
                            0.590243902,
                            0.530612245,
                            0.408256881,
                            0.132867133, 0
]
RWC_gravimetric_One50_2 = [0.959183673,
                            0.867132867,
                            0.518716578,
                            0.347280335,
                            0.307692308,
                            0.295918367, 0
]
# RWC_gravimetric_GA66_1 = [98.4,99.3,97.7,95.5,95.4,96.6]
# RWC_gravimetric_GA66_2 = [99.0,95.7,96.7,94.3,90.2,95.6]

# Plotting dH20 for each group
fig, axs = plt.subplots(1, 2, figsize=(12, 8))
fig.suptitle('RWC_gravimetric for Each Group')

# 使用正确的子图索引
axs[0].plot(range(1, times+1), RWC_gravimetric_One50_1, marker='o')
axs[0].set_title('One50-1')
axs[0].set_xlabel('Day')
axs[0].set_ylabel('RWC_gravimetric (%)')

axs[1].plot(range(1, times+1), RWC_gravimetric_One50_2, marker='o')
axs[1].set_title('One50-2')
axs[1].set_xlabel('Day')
axs[1].set_ylabel('RWC_gravimetric (%)')

plt.tight_layout()
plt.show()

# %%
# plot RWC_THz and RWC_gravimetric
import matplotlib.pyplot as plt

# plot
fig, axs = plt.subplots(1, 2, figsize=(12, 8))
fig.suptitle('RWC Comparisons for Each Group')

# One50-1
axs[0].plot(range(1, times+1), RWC_gravimetric_One50_1, marker='o', color='blue', label='RWC_gravimetric')
axs[0].plot(range(1, times+1), RWC_THz_One50_1, marker='o', color='red', label='RWC_THz')
axs[0].set_title('One50-1')
axs[0].set_xlabel('Day')
axs[0].set_ylabel('RWC (%)')
axs[0].legend()

# One50-2
axs[1].plot(range(1, times+1), RWC_gravimetric_One50_2, marker='o', color='blue', label='RWC_gravimetric')
axs[1].plot(range(1, times+1), RWC_THz_One50_2, marker='o', color='red', label='RWC_THz')
axs[1].set_title('One50-2')
axs[1].set_xlabel('Day')
axs[1].set_ylabel('RWC (%)')
axs[1].legend()

plt.tight_layout()
plt.show()

# %%
