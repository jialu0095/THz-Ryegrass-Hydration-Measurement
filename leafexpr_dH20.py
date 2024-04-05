import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('leaf_expr_API')

def calculate_dH20(I_ref, I_smp, dB_ref, dB_smp):
    I_ref = np.array(I_ref)
    I_smp = np.array(I_smp)
    dB_ref = np.array(dB_ref)
    dB_smp = np.array(dB_smp)
    
    d_H20 = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / 85

    # remove -inf nan values
    valid_values_mean = np.nanmean(np.where(d_H20 == -np.inf, np.nan, d_H20))
    d_H20 = np.where(np.isneginf(d_H20) | np.isnan(d_H20), valid_values_mean, d_H20)

    return d_H20

time = []
dry_time = 12
for i in range(dry_time):
    time.append(i+1)

# expr data
wet_weight = [0.7876, 0.7704, 0.7540, 0.7392, 0.7247, 0.7114, 0.6966, 0.6822, 0.6669, 0.6501, 0.6357, 0.5828]
dry_weight = [0.5828, 0.5828, 0.5828, 0.5828, 0.5828, 0.5828, 0.5828, 0.5828, 0.5828, 0.5828, 0.5828, 0.5828]

wet_attenuation = [0.5, 0.5, 0.4, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.7, 1.7, 2.7]
dry_attenuation = [2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7]

wet_pixel = [0.476, 0.49, 0.492, 0.494, 0.496, 0.494, 0.499, 0.493, 0.495, 0.496, 0.499, 0.496]
dry_pixel = [0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496, 0.496]

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

I_refs = np.loadtxt('dry.txt', delimiter=' ', comments='#').flatten()
dB_refs = np.repeat(dB_ref[0], len(I_refs))
for i in range(dry_time-1):
    # get data
    I_smps = np.loadtxt('wet' + str(i+1) + '.txt', delimiter=' ', comments='#').flatten()
    dB_smps = np.repeat(dB_smp[i], len(I_smps))

    # dH20 mean
    dH20_all = calculate_dH20(I_refs, I_smps, dB_refs, dB_smps)
    

    dH20_all[dH20_all < 0] = np.mean(dH20_all)

    RWC_THz_all = dH20_all/dH20_all[0] * 100
    print(RWC_THz_all)
    RWC_THz_std_all = np.std(RWC_THz_all)
    # print(RWC_THz_std_all)
    # print(dH20_all)

    dH20 = np.mean(dH20_all)
    dH20_std = np.std(calculate_dH20(I_refs, I_smps, dB_refs, dB_smps))
    
    dH20s.append(dH20)
    dH20_stds.append(dH20_std)
    RWC_THz_std_alls.append(RWC_THz_std_all)

dH20s.append(0)
dH20_stds.append(0)
RWC_THz_std_alls.append(0)
print(len(RWC_THz_std_alls))
print(RWC_THz_std_alls)

# # RWC with THz
# dH20 = calculate_dH20(I_ref, I_smp, dB_ref, dB_smp)
dH20 = dH20s
RWC_THz = dH20/dH20[0] * 100
print(RWC_THz)


# RWC with gravimetric balance
RWC_gravimetric = (wet_weight - dry_weight) / (wet_weight[0] - dry_weight) * 100

plt.subplot(2, 1, 1)
plt.scatter(time, RWC_gravimetric, label='Gravimetric', color='black')
# plt.errorbar(time, RWC_THz, yerr=np.array(RWC_THz_std_alls), color='green')  # Fix: Convert RWC_THz_std to a numpy array
plt.scatter(time, RWC_THz, label='THz', color='green')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('RWC vs Time')
plt.legend()
plt.tight_layout()
# plt.show()

plt.subplot(2, 1, 2)
plt.scatter(time, dH20, label='dH20', color='red')
# plt.errorbar(time, dH20, yerr=dH20_stds, label='dH20', color='red')
plt.xlabel('Time')
plt.ylabel('d_H20')
plt.title('d_H20 vs Time')
plt.legend()
plt.tight_layout()
plt.show()
