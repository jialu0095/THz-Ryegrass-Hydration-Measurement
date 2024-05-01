import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.chdir('plant_expr_API/day1')

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
# Read the CSV file
dB_dry = pd.read_csv('dB_dry1_one55-2.csv')
dB_wet = pd.read_csv('dB_wet1_one55-2.csv')
dB_tur = pd.read_csv('dB_tur1_one55-2.csv')
dB_dry = [11.7]*len(dB_dry)

I_dry = pd.read_csv('I_dry1_one55-2.csv')
I_wet = pd.read_csv('I_wet1_one55-2.csv')
I_tur = pd.read_csv('I_tur1_one55-2.csv')

# Rest of the code...
d_H20_sat = calculate_dH20(I_dry, I_tur, dB_dry, dB_tur)
d_H20_wet = calculate_dH20(I_dry, I_wet, dB_dry, dB_wet)

RWC_THz = 100 * d_H20_wet / d_H20_sat

print(np.mean(RWC_THz))
print(np.std(RWC_THz))
# %%
