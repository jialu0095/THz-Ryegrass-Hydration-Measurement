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

def print_mean_I(I_group, group_name):
    for i in range(0,5):
        I = I_group[i]
        I = np.array(I)
        zero_indices = np.where(I == 0)[0]
        I = np.delete(I, zero_indices)
        I_mean = np.mean(I)
        print(f'{group_name} day {i+1} mean I: ', I_mean)


#%%
# load THz data
I_One50_1 = [[],[],[],[],[]]
I_One50_2 = [[],[],[],[],[]]
I_One50_3 = [[],[],[],[],[]]
I_GA66_1 = [[],[],[],[],[]]
I_GA66_2 = [[],[],[],[],[]]
I_GA66_3 = [[],[],[],[],[]]

dB_One50_1 = [[],[],[],[],[]]
dB_One50_2 = [[],[],[],[],[]]
dB_One50_3 = [[],[],[],[],[]]
dB_GA66_1 = [[],[],[],[],[]]
dB_GA66_2 = [[],[],[],[],[]]
dB_GA66_3 = [[],[],[],[],[]]

for i in range(0,5):
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
dH20_One50_1 = [[],[],[],[],[]]
dH20_One50_2 = [[],[],[],[],[]]
dH20_One50_3 = [[],[],[],[],[]]
dH20_GA66_1 = [[],[],[],[],[]]
dH20_GA66_2 = [[],[],[],[],[]]
dH20_GA66_3 = [[],[],[],[],[]]

print(I_One50_1[-1])
print(I_One50_1[0])

for i in range(0,5):
    print(i)
    dH20_One50_1[i] = calculate_dH20_plant(I_One50_1[-1], I_One50_1[i], dB_One50_1[-1], dB_One50_1[i], i+1)
    dH20_One50_2[i] = calculate_dH20_plant(I_One50_2[-1], I_One50_2[i], dB_One50_2[-1], dB_One50_2[i], i+1)
    dH20_One50_3[i] = calculate_dH20_plant(I_One50_3[-1], I_One50_3[i], dB_One50_3[-1], dB_One50_3[i], i+1)
    dH20_GA66_1[i] = calculate_dH20_plant(I_GA66_1[-1], I_GA66_1[i], dB_GA66_1[-1], dB_GA66_1[i], i+1)
    dH20_GA66_2[i] = calculate_dH20_plant(I_GA66_2[-1], I_GA66_2[i], dB_GA66_2[-1], dB_GA66_2[i], i+1)
    dH20_GA66_3[i] = calculate_dH20_plant(I_GA66_3[-1], I_GA66_3[i], dB_GA66_3[-1], dB_GA66_3[i], i+1)

#%% 

print_mean_I(I_GA66_1, 'GA66-1')
print_mean_I(I_GA66_2, 'GA66-2')
print_mean_I(I_GA66_3, 'GA66-3')
print_mean_I(I_One50_1, 'One50-1')
print_mean_I(I_One50_2, 'One50-2')
print_mean_I(I_One50_3, 'One50-3')


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
RWC_gravimetric_One50_1 = [97.5,98.9,95.7,94.3,93.5]
RWC_gravimetric_One50_2 = [99.5,96.2,90.9,91.3,89.7]
RWC_gravimetric_One50_3 = [99.0,97.3,94.2,93.2,90.2]
RWC_gravimetric_GA66_1 = [98.4,99.3,97.7,95.5,95.4]
RWC_gravimetric_GA66_2 = [99.0,95.7,96.7,94.3,90.2]
RWC_gravimetric_GA66_3 = [99.4,96.7,92.7,90.3,88.9]