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
I_refs = np.loadtxt('I_refs_05', delimiter=',', comments='#')
I_smps = np.loadtxt('I_smps_05', delimiter=',', comments='#')
dB_refs = np.loadtxt('dB_refs_05', delimiter=',', comments='#')
dB_smps = np.loadtxt('dB_smps_05', delimiter=',', comments='#')

# I_refs = np.loadtxt('I_refs_02', delimiter=',', comments='#')
# I_smps = np.loadtxt('I_smps_02', delimiter=',', comments='#')
# dB_refs = np.loadtxt('dB_refs_02', delimiter=',', comments='#')
# dB_smps = np.loadtxt('dB_smps_02', delimiter=',', comments='#')


print(I_refs)
print(I_smps)
print(dB_refs)
print(dB_smps)
#%%
d_H2O = 0.05
# d_H2O = 0.02
alpha = calculate_alpha(I_refs, I_smps, dB_refs, dB_smps, d_H2O)

print(alpha)
# %%
with open('output_05.txt', 'w') as f:
    f.write('average of alpha: ' + str(np.mean(alpha)) + '\n')
    f.write('standard deviation of alpha: ' + str(np.std(alpha)) + '\n')
    for i in range(len(alpha)):
        f.write(f'alpha[{i}]: {alpha[i]}\n')
        f.write(f'I_refs[{i}]: {I_refs[i]}\n')
        f.write(f'dB_refs[{i}]: {dB_refs[i]}\n')
        f.write(f'I_smps[{i}]: {I_smps[i]}\n')
        f.write(f'dB_smps[{i}]: {dB_smps[i]}\n')
        f.write('---------------------------------\n')

# %%
alpha_std = np.std(alpha)
print("Standard Deviation of alpha:", alpha_std)
alpha_avg = np.mean(alpha)
print("Average of alpha:", alpha_avg)
# %%
