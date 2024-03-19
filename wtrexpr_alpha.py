#%%
import numpy as np
import os

# change working dir
os.chdir('water_layer_expr_API')
print(os.getcwd())

def calculate_alpha(I_ref, I_smp, dB_ref, dB_smp, d_H2O):
    alpha = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / d_H2O
    return alpha

#%%
I_refs = np.loadtxt('I_refs', delimiter=',', comments='#')
I_smps = np.loadtxt('I_smps', delimiter=',', comments='#')
dB_refs = np.loadtxt('dB_refs', delimiter=',', comments='#')
dB_smps = np.loadtxt('dB_smps', delimiter=',', comments='#')

d_H2O = 0.05
alpha = calculate_alpha(I_refs, I_smps, dB_refs, dB_smps, d_H2O)