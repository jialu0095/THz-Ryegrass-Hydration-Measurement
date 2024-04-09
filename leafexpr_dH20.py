#%%
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('leaf_expr_API')

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
# time for drying up the leaves
time = []
dry_time = 11
time_lap = 4
for i in range(dry_time):
    time.append((i+1)*4)

# expr data
wet_weight = [0.8144, 0.7482, 0.6678, 0.6007, 0.5231, 0.4371, 0.3442, 0.2523, 0.1839, 0.1528, 0.1415]
dry_weight = [0.1415, 0.1415, 0.1415, 0.1415, 0.1415, 0.1415, 0.1415, 0.1415, 0.1415, 0.1415, 0.1415]

wet_attenuation = [0.1, 0.5, 1.9, 4, 5.2, 6.2, 7.6, 9.5, 10.4, 10.9, 11.5]
dry_attenuation = [11.5, 11.5, 11.5, 11.5, 11.5, 11.5, 11.5, 11.5, 11.5, 11.5, 11.5]

wet_pixel = [0.438, 0.485, 0.498, 0.494, 0.499, 0.499, 0.497, 0.499, 0.498, 0.493, 0.496]
dry_pixel = [0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496]


# expr variables
fresh_weight = 0.9192
wet_weight = np.array(wet_weight)
dry_weight = np.array(dry_weight)

I_smp = wet_pixel
dB_smp = wet_attenuation
I_ref = dry_pixel
dB_ref = dry_attenuation
dH20s = []
dH20_stds = []
RWC_THz_std_alls = []
RWC_THz_means = []

for i in range(dry_time):
    # get data
    I_smps = np.loadtxt('wet' + str(i+1) + '.txt', delimiter=' ', comments='#').flatten()
    if i == 10:
        I_smps = np.loadtxt('dry.txt', delimiter=' ', comments='#').flatten()
    
    I_refs = np.loadtxt('dry.txt', delimiter=' ', comments='#').flatten()
    
    # delete elements with same index of I_smps in I_refs
    del_index = np.where(I_smps < 0.5)
    
    # delete saturated points
    # I_refs[del_index] = 0.5
    # I_smps[del_index] = 0.5
    # I_refs = np.delete(I_refs, del_index)
    # I_smps = np.delete(I_smps, del_index)

    dB_smps = np.repeat(dB_smp[i], len(I_smps))
    dB_refs = np.repeat(dB_ref[0], len(I_refs))

    # dH20 mean
    dH20_all = calculate_dH20(I_refs, I_smps, dB_refs, dB_smps)

    # first dH20 as variable
    if(i == 0):
        dH20_wet1 = dH20_all

    # deal with calculate error
    if dH20_all[0] != 0:
        RWC_THz_all = dH20_all/dH20_wet1 * 100
    else:
        RWC_THz_all = np.repeat(0, len(dH20_all))
    RWC_THz_mean = np.mean(RWC_THz_all)
    RWC_THz_std_all = np.std(RWC_THz_all)

    dH20 = np.mean(dH20_all)
    dH20_std = np.std(calculate_dH20(I_refs, I_smps, dB_refs, dB_smps))
    
    dH20s.append(dH20)
    dH20_stds.append(dH20_std)
    RWC_THz_std_alls.append(RWC_THz_std_all)
    RWC_THz_means.append(RWC_THz_mean)


# RWC with gravimetric balance
RWC_gravimetric = (wet_weight - dry_weight) / (wet_weight[0] - dry_weight) * 100

plt.subplot(2, 1, 1)
plt.scatter(time, RWC_gravimetric, label='Gravimetric', color='black')
plt.errorbar(time, RWC_THz_means, yerr=RWC_THz_std_alls, color='green', fmt='o')
plt.scatter(time, RWC_THz_means, label='THz', color='green')
plt.xlabel('Dry Time[min]')
plt.ylabel('Relative Water Content[%]')
plt.title('RWC aginst Dry Time for Single Leaf')
plt.legend()
plt.tight_layout()
# plt.show()

plt.subplot(2, 1, 2)
plt.errorbar(time, dH20s, yerr=dH20_stds, color='red', fmt='o')
plt.scatter(time, dH20s, label=r'$d_{H20}$', color='red')
plt.xlabel('Dry Time[min]')
plt.ylabel(r'$d_{H20}$['+dH20_unit+']')
plt.title(r'Water Layer Thickness aginst Dry Time for Single Leaf')
plt.legend()
plt.tight_layout()
plt.show()

#%%