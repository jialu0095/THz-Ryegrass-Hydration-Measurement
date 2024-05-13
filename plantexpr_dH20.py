#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.chdir('plant_expr_API/all_plant_data')

#%%
# output: dH20(mm)
dH20_unit = 'mm'
def calculate_dH20_plant(I_ref, I_smp, dB_ref, dB_smp, group):
    I_ref = np.array(I_ref)
    I_smp = np.array(I_smp)
    dB_ref = np.array(dB_ref)
    dB_smp = np.array(dB_smp)

    zero_indices = np.where((I_ref == 0) | (I_smp == 0))[0]
    print('empty pixels: ', len(zero_indices))
    I_ref = np.delete(I_ref, zero_indices)
    I_smp = np.delete(I_smp, zero_indices)
    dB_ref = np.delete(dB_ref, zero_indices)
    dB_smp = np.delete(dB_smp, zero_indices)

    I_mean_ref = np.mean(I_ref)
    if(group == 5):
        I_mean_smp = np.mean(I_smp)
    else:
        I_mean_smp = np.mean(I_smp) - np.mean(I_smp)/1.3
    dB_mean_ref = np.mean(dB_ref)
    dB_mean_smp = np.mean(dB_smp)
    
    dH20 = (np.log(I_mean_ref / I_mean_smp) + 0.1*np.log(10) * (dB_mean_ref - dB_mean_smp)) / 85 # cm
    # dH20 = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / 85 # cm
    dH20 *= 10 # cm to mm
    # mm to um
    if dH20_unit == 'um':
        dH20 *= 1000

    # remove -inf nan values
    valid_values_mean = np.nanmean(np.where(dH20 == -np.inf, np.nan, dH20))
    dH20 = np.where(np.isneginf(dH20) | np.isnan(dH20), valid_values_mean, dH20)

    return dH20

def print_mean_I0(I_group, group_name, dB_group, dB_name, current_day):
    for i in range(0,current_day):
        I = I_group[i]
        dB = dB_group[i]
        zero_indices = np.where(I == 0)[0]
        I = np.delete(I, zero_indices)
        dB = np.delete(dB, zero_indices)
        I_0 = 10**(dB/10)*I
        I_0_mean = np.mean(I_0)
        print(f'{group_name} day {i+1} mean I_0: ', I_0_mean)

def cal_mean_I0(I_group, group_name, dB_group, dB_name, current_day):
    I_0_means = []
    for i in range(0,current_day):
        I = I_group[i]
        dB = dB_group[i]
        zero_indices = np.where(I == 0)[0]
        I = np.delete(I, zero_indices)
        dB = np.delete(dB, zero_indices)
        I_0 = 10**(dB/10)*I
        I_0_mean = np.mean(I_0)
        I_0_means.append(I_0_mean)
    return I_0_means


# %%
current_day = 8

#%%
# load THz data
I_One50_1 = [[] for _ in range(current_day)]
I_One50_2 = [[] for _ in range(current_day)]
I_One50_3 = [[] for _ in range(current_day)]
I_GA66_1 = [[] for _ in range(current_day)]
I_GA66_2 = [[] for _ in range(current_day)]
I_GA66_3 = [[] for _ in range(current_day)]

dB_One50_1 = [[] for _ in range(current_day)]
dB_One50_2 = [[] for _ in range(current_day)]
dB_One50_3 = [[] for _ in range(current_day)]
dB_GA66_1 = [[] for _ in range(current_day)]
dB_GA66_2 = [[] for _ in range(current_day)]
dB_GA66_3 = [[] for _ in range(current_day)]

for i in range(0,current_day):
    print(i)
    I_One50_1[i] = np.loadtxt('I_wet'+str(i+1)+'_One50_1.csv', delimiter=' ', comments='#')
    I_One50_2[i] = np.loadtxt('I_wet'+str(i+1)+'_One50_2.csv', delimiter=' ', comments='#')
    I_One50_3[i] = np.loadtxt('I_wet'+str(i+1)+'_One50_3.csv', delimiter=' ', comments='#')
    I_GA66_1[i] = np.loadtxt('I_wet'+str(i+1)+'_GA66_1.csv', delimiter=' ', comments='#')
    I_GA66_2[i] = np.loadtxt('I_wet'+str(i+1)+'_GA66_2.csv', delimiter=' ', comments='#')
    I_GA66_3[i] = np.loadtxt('I_wet'+str(i+1)+'_GA66_3.csv', delimiter=' ', comments='#')

    dB_One50_1[i] = np.loadtxt('dB_wet'+str(i+1)+'_One50_1.csv', delimiter=' ', comments='#')
    dB_One50_2[i] = np.loadtxt('dB_wet'+str(i+1)+'_One50_2.csv', delimiter=' ', comments='#')
    dB_One50_3[i] = np.loadtxt('dB_wet'+str(i+1)+'_One50_3.csv', delimiter=' ', comments='#')
    dB_GA66_1[i] = np.loadtxt('dB_wet'+str(i+1)+'_GA66_1.csv', delimiter=' ', comments='#')
    dB_GA66_2[i] = np.loadtxt('dB_wet'+str(i+1)+'_GA66_2.csv', delimiter=' ', comments='#')
    dB_GA66_3[i] = np.loadtxt('dB_wet'+str(i+1)+'_GA66_3.csv', delimiter=' ', comments='#')



#%%
# calculate dH20
dH20_One50_1 = [[] for _ in range(current_day)]
dH20_One50_2 = [[] for _ in range(current_day)]
dH20_One50_3 = [[] for _ in range(current_day)]
dH20_GA66_1 = [[] for _ in range(current_day)]
dH20_GA66_2 = [[] for _ in range(current_day)]
dH20_GA66_3 = [[] for _ in range(current_day)]


for i in range(0,current_day):
    print(i)
    dH20_One50_1[i] = calculate_dH20_plant(I_One50_1[-1], I_One50_1[i], dB_One50_1[-1], dB_One50_1[i], i+1)
    dH20_One50_2[i] = calculate_dH20_plant(I_One50_2[-1], I_One50_2[i], dB_One50_2[-1], dB_One50_2[i], i+1)
    dH20_One50_3[i] = calculate_dH20_plant(I_One50_3[-1], I_One50_3[i], dB_One50_3[-1], dB_One50_3[i], i+1)
    dH20_GA66_1[i] = calculate_dH20_plant(I_GA66_1[-1], I_GA66_1[i], dB_GA66_1[-1], dB_GA66_1[i], i+1)
    dH20_GA66_2[i] = calculate_dH20_plant(I_GA66_2[-1], I_GA66_2[i], dB_GA66_2[-1], dB_GA66_2[i], i+1)
    dH20_GA66_3[i] = calculate_dH20_plant(I_GA66_3[-1], I_GA66_3[i], dB_GA66_3[-1], dB_GA66_3[i], i+1)


#%%
print_mean_I0(I_GA66_1, 'GA66-1', dB_GA66_1, 'GA66-1', current_day)
print_mean_I0(I_GA66_2, 'GA66-2', dB_GA66_2, 'GA66-2', current_day)
print_mean_I0(I_GA66_3, 'GA66-3', dB_GA66_3, 'GA66-3', current_day)
print_mean_I0(I_One50_1, 'One50-1', dB_One50_1, 'One50-1', current_day)
print_mean_I0(I_One50_2, 'One50-2', dB_One50_2, 'One50-2', current_day)
print_mean_I0(I_One50_3, 'One50-3', dB_One50_3, 'One50-3', current_day)

I_GA66_1_I0 = cal_mean_I0(I_GA66_1, 'GA66-1', dB_GA66_1, 'GA66-1', current_day)
I_GA66_2_I0 = cal_mean_I0(I_GA66_2, 'GA66-2', dB_GA66_2, 'GA66-2', current_day)
I_GA66_3_I0 = cal_mean_I0(I_GA66_3, 'GA66-3', dB_GA66_3, 'GA66-3', current_day)
I_One50_1_I0 = cal_mean_I0(I_One50_1, 'One50-1', dB_One50_1, 'One50-1', current_day)
I_One50_2_I0 = cal_mean_I0(I_One50_2, 'One50-2', dB_One50_2, 'One50-2', current_day)
I_One50_3_I0 = cal_mean_I0(I_One50_3, 'One50-3', dB_One50_3, 'One50-3', current_day)

# Plotting I0 for each group
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('I0 for Each Group')

axs[0, 0].plot(range(1, current_day+1), I_GA66_1_I0, marker='o')
axs[0, 0].set_title('GA66-1')
axs[0, 0].set_xlabel('Day')
axs[0, 0].set_ylabel('I0')

axs[0, 1].plot(range(1, current_day+1), I_GA66_2_I0, marker='o')
axs[0, 1].set_title('GA66-2')
axs[0, 1].set_xlabel('Day')
axs[0, 1].set_ylabel('I0')

axs[0, 2].plot(range(1, current_day+1), I_GA66_3_I0, marker='o')
axs[0, 2].set_title('GA66-3')
axs[0, 2].set_xlabel('Day')
axs[0, 2].set_ylabel('I0')

axs[1, 0].plot(range(1, current_day+1), I_One50_1_I0, marker='o')
axs[1, 0].set_title('One50-1')
axs[1, 0].set_xlabel('Day')
axs[1, 0].set_ylabel('I0')

axs[1, 1].plot(range(1, current_day+1), I_One50_2_I0, marker='o')
axs[1, 1].set_title('One50-2')
axs[1, 1].set_xlabel('Day')
axs[1, 1].set_ylabel('I0')

axs[1, 2].plot(range(1, current_day+1), I_One50_3_I0, marker='o')
axs[1, 2].set_title('One50-3')
axs[1, 2].set_xlabel('Day')
axs[1, 2].set_ylabel('I0')

plt.tight_layout()
plt.show()

#%%
print(dH20_One50_1)
print(dH20_One50_2) 
print(dH20_One50_3)
print(dH20_GA66_1)
print(dH20_GA66_2)
print(dH20_GA66_3)

# RWC_THz_One50_1 = dH20_One50_1/dH20_One50_1[-1]

# %%
# gravimetric data
RWC_gravimetric_One50_1 = [97.5,98.9,95.7,94.3,93.5,96.3]
RWC_gravimetric_One50_2 = [99.5,96.2,90.9,91.3,89.7,97.8]
RWC_gravimetric_One50_3 = [99.0,97.3,94.2,93.2,90.2,92.7]
RWC_gravimetric_GA66_1 = [98.4,99.3,97.7,95.5,95.4,96.6]
RWC_gravimetric_GA66_2 = [99.0,95.7,96.7,94.3,90.2,95.6]
RWC_gravimetric_GA66_3 = [99.4,96.7,92.7,90.3,88.9,99.5]

# Plotting dH20 for each group
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('dH20 for Each Group')

axs[0, 0].plot(range(1, current_day+1), RWC_gravimetric_GA66_1, marker='o')
axs[0, 0].set_title('GA66-1')
axs[0, 0].set_xlabel('Day')
axs[0, 0].set_ylabel('RWC_gravimetric (%)')

axs[0, 1].plot(range(1, current_day+1), RWC_gravimetric_GA66_2, marker='o')
axs[0, 1].set_title('GA66-2')
axs[0, 1].set_xlabel('Day')
axs[0, 1].set_ylabel('RWC_gravimetric (%)')

axs[0, 2].plot(range(1, current_day+1), RWC_gravimetric_GA66_3, marker='o')
axs[0, 2].set_title('GA66-3')
axs[0, 2].set_xlabel('Day')
axs[0, 2].set_ylabel('RWC_gravimetric (%)')

axs[1, 0].plot(range(1, current_day+1), RWC_gravimetric_One50_1, marker='o')
axs[1, 0].set_title('One50-1')
axs[1, 0].set_xlabel('Day')
axs[1, 0].set_ylabel('RWC_gravimetric (%)')

axs[1, 1].plot(range(1, current_day+1), RWC_gravimetric_One50_2, marker='o')
axs[1, 1].set_title('One50-2')
axs[1, 1].set_xlabel('Day')
axs[1, 1].set_ylabel('RWC_gravimetric (%)')

axs[1, 2].plot(range(1, current_day+1), RWC_gravimetric_One50_3, marker='o')
axs[1, 2].set_title('One50-3')
axs[1, 2].set_xlabel('Day')
axs[1, 2].set_ylabel('RWC_gravimetric (%)')

plt.tight_layout()
plt.show()
# %%
