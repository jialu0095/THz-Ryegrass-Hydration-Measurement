#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import uncertainties.unumpy as unumpy

# os.chdir('plant_expr_API/One50_data')
os.chdir('plant_expr_API/GA66_data')
# os.chdir('plant_expr_API')

#%%
# output: dH20(mm)
dH20_unit = 'mm'
def calculate_dH20_plant(I_ref, I_smp, dB_ref, dB_smp, group):
    # ref: dry, smp: wet

    # I_ref = np.array(I_ref)
    # I_smp = np.array(I_smp)
    # dB_ref = np.array(dB_ref)
    # dB_smp = np.array(dB_smp)

    # remove empty pixels
    zero_indices = np.where((I_ref == 0) | (I_smp == 0))[0]
    print('empty pixels: ', len(zero_indices))
    I_ref = np.delete(I_ref, zero_indices)
    I_smp = np.delete(I_smp, zero_indices)
    dB_ref = np.delete(dB_ref, zero_indices)
    dB_smp = np.delete(dB_smp, zero_indices)

    # get std value to add uncertainty
    I_std_ref = np.std(I_ref)
    I_std_smp = np.std(I_smp)
    dB_std_ref = np.std(dB_ref)
    dB_std_smp = np.std(dB_smp)

    I_ref = unumpy.uarray(I_ref, [I_std_ref]*len(I_ref))
    I_smp = unumpy.uarray(I_smp, [I_std_smp]*len(I_smp))
    dB_ref = unumpy.uarray(dB_ref, [dB_std_ref]*len(dB_ref))
    dB_smp = unumpy.uarray(dB_smp, [dB_std_smp]*len(dB_smp))

    # # get mean value
    I_mean_ref = np.mean(I_ref)
    I_mean_smp = np.mean(I_smp)
    dB_mean_ref = np.mean(dB_ref)
    dB_mean_smp = np.mean(dB_smp)

    # print(f'dB_mean_smpl: {dB_mean_smp}')
    
    # calculate dH20
    dH20 = (unumpy.log(I_mean_ref / I_mean_smp) + 0.1*unumpy.log(10) * (dB_mean_ref - dB_mean_smp)) / 85 # cm
    dH20 *= 10 # cm to mm
    # mm to um
    if dH20_unit == 'um':
        dH20 *= 1000

    # remove -inf nan values
    # valid_values_mean = np.nanmean(np.where(dH20 == -np.inf, np.nan, dH20))
    # dH20 = np.where(np.isneginf(dH20) | np.isnan(dH20), valid_values_mean, dH20)

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

# def cal_RWC_THz(dH20, dH20_max):
#     RWC_THz = dH20/dH20_max
#     return RWC_THz

def cal_RWC_THz(dH20, dH20_max):
    RWC_THz = [d / dH20_max for d in dH20]
    return RWC_THz


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
    print(f'{species}-{plant_number} RWC_THz: ', RWC_THz)
    # return RWC_THz
    return RWC_THz

# %%
# One50-3
times = 13
# THz_results('One50', '3', times)
RWC_THz_One50_3 = THz_results('One50', '3', times)

# get nominal values    
RWC_THz_One50_3_nominal = unumpy.nominal_values(RWC_THz_One50_3)
# get std values
RWC_THz_One50_3_std = unumpy.std_devs(RWC_THz_One50_3)
RWC_THz_One50_3_std[-1] = 0

# x-axis values: times
x_values = range(1, times + 1)

# plot
plt.figure(figsize=(10, 5))  # fig size
plt.errorbar(x_values, RWC_THz_One50_3_nominal, yerr=RWC_THz_One50_3_std, fmt='o', label='One50-3', capsize=5, elinewidth=2, markeredgewidth=2)
plt.title('Plant One50-3')
plt.xlabel('Time [/20mins]')
plt.ylabel('RWC_THz [%]')
plt.legend()  
plt.grid(False)  
plt.tight_layout()  
plt.show()

#%%

# One50-1, One50-2 THz RWC results
times = 7
# THz_results('One50', '3', times)
RWC_THz_One50_1 = THz_results('One50', '1', times)
RWC_THz_One50_2 = THz_results('One50', '2', times)

# One50_1 and One50_2 gravimetric data
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

# Adjust the standard deviation of each measurement based on the size of this deviation 
# to better reflect this uncertainty

RWC_THz_One50_1_nominal = unumpy.nominal_values(RWC_THz_One50_1)
RWC_THz_One50_2_nominal = unumpy.nominal_values(RWC_THz_One50_2)

# additional error factor
additional_error_factor_One50_1 = abs(RWC_gravimetric_One50_1[0] - RWC_THz_One50_1_nominal[0]) / RWC_THz_One50_1_nominal[0]
additional_error_factor_One50_2 = abs(RWC_gravimetric_One50_2[0] - RWC_THz_One50_2_nominal[0]) / RWC_THz_One50_2_nominal[0]

RWC_THz_One50_1_std = unumpy.std_devs(RWC_THz_One50_1) * (1 + additional_error_factor_One50_1)
RWC_THz_One50_2_std = unumpy.std_devs(RWC_THz_One50_2) * (1 + additional_error_factor_One50_2)

RWC_THz_One50_1_std[-1] = 0
RWC_THz_One50_2_std[-1] = 0


# x-axis values: times
x_values = range(1, times + 1)


# %%


# Plotting RWC_THz for each group with error bars
fig, axs = plt.subplots(2, 1, figsize=(12, 12))
fig.suptitle('RWC_THz for Each Group')

# Plot for One50-1 with error bars
axs[0].scatter(range(1, times+1), RWC_gravimetric_One50_1, marker='o', color='red', label='RWC_gravimetric')
axs[0].errorbar(x_values, RWC_THz_One50_1_nominal, yerr=RWC_THz_One50_1_std, fmt='o', label='RWC_THz', capsize=5)
axs[0].set_title('Plant One50-1')
axs[0].set_xlabel('Time [/20mins]')
axs[0].set_ylabel('RWC_THz [%]')
axs[0].legend()

# Plot for One50-2 with error bars
axs[1].scatter(range(1, times+1), RWC_gravimetric_One50_2, marker='o', color='red', label='RWC_gravimetric')
axs[1].errorbar(x_values, RWC_THz_One50_2_nominal, yerr=RWC_THz_One50_2_std, fmt='o', label='RWC_THz', capsize=5)
axs[1].set_title('Plant One50-2')
axs[1].set_xlabel('Time [/20mins]')
axs[1].set_ylabel('RWC_THz [%]')
axs[1].legend()

plt.tight_layout()
plt.show()




# %% 
# seperate plot for One50-1 and One50-2
plt.figure(figsize=(12, 6))
plt.scatter(range(1, times+1), RWC_gravimetric_One50_1, marker='o', color='red', label='RWC_gravimetric')
plt.errorbar(x_values, RWC_THz_One50_1_nominal, yerr=RWC_THz_One50_1_std, fmt='o', label='RWC_THz', capsize=5)
plt.title('Plant One50-1 RWC Analysis')
plt.xlabel('Time [/20mins]')
plt.ylabel('RWC_THz [%]')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.scatter(range(1, times+1), RWC_gravimetric_One50_2, marker='o', color='red', label='RWC_gravimetric')
plt.errorbar(x_values, RWC_THz_One50_2_nominal, yerr=RWC_THz_One50_2_std, fmt='o', label='RWC_THz', capsize=5)
plt.title('Plant One50-2 RWC Analysis')
plt.xlabel('Time [/20mins]')
plt.ylabel('RWC_THz [%]')
plt.legend()
plt.tight_layout()
plt.show()

# %%
