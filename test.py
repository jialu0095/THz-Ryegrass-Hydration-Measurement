#%%
import numpy as np
import os

# change working dir
os.chdir('water_layer_expr_API')
print(os.getcwd())

def calculate_alpha(I_ref, I_smp, dB_ref, dB_smp, d_H2O):
    alpha = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / d_H2O
    return alpha

def calculate_d_H2O(I_ref, I_smp, dB_ref, dB_smp, alpha):
    d_H2O = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / alpha
    return d_H2O

#%%
I_refs = np.loadtxt('I_refs_02', delimiter=',', comments='#')
I_smps = np.loadtxt('I_smps_02', delimiter=',', comments='#')
dB_refs = np.loadtxt('dB_refs_02', delimiter=',', comments='#')
dB_smps = np.loadtxt('dB_smps_02', delimiter=',', comments='#')

d_H20s = calculate_d_H2O(I_refs, I_smps, dB_refs, dB_smps, 85)
print(d_H20s)
# %%

# %%
