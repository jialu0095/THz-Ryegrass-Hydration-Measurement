#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.chdir('plant_expr_API')

#%%
# output: dH20(mm)
dH20_unit = 'mm'
def calculate_dH20(I_ref, I_smp, dB_ref, dB_smp):
    I_ref = np.array(I_ref)
    I_smp = np.array(I_smp)
    dB_ref = np.array(dB_ref)
    dB_smp = np.array(dB_smp)
    
    dH20 = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / 85 # cm
    dH20 *= 10 # cm to mm
    # mm to um
    if dH20_unit == 'um':
        dH20 *= 1000

    # remove -inf nan values
    valid_values_mean = np.nanmean(np.where(dH20 == -np.inf, np.nan, dH20))
    dH20 = np.where(np.isneginf(dH20) | np.isnan(dH20), valid_values_mean, dH20)

    return dH20

#%%
I_wet = np.loadtxt('I_wet1_One50_1.csv', delimiter=' ', comments='#')
dB_wet = np.loadtxt('dB_wet1_One50_1.csv', delimiter=' ', comments='#')
index = I_wet <= 0

I_wet = I_wet[~index]
dB_wet = dB_wet[~index]

print('mean: ', np.mean(I_wet))
print('std: ', np.std(I_wet))  

number_not_0 = np.count_nonzero(I_wet)
print('number_not_0: ', number_not_0)

# %%
