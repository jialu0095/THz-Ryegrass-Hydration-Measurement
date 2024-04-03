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
dry_time = 10
for i in range(dry_time):
    time.append(i+1)

# expr data
wet_weight = [0.9313,0.9080,0.8865,0.8670,0.8470,0.8225,0.8035,0.7835,0.7676,0.2208]
dry_weight = [0.2208,0.2208,0.2208,0.2208,0.2208,0.2208,0.2208,0.2208,0.2208,0.2208]

wet_attenuation = [1.6,1.6,1.8,1.8,2.1,2.1,2.2,2.4,2.5,11.5]
dry_attenuation = [11.5,11.5,11.5,11.5,11.5,11.5,11.5,11.5,11.5,11.5]

wet_pixel = [0.498,0.494,0.474,0.496,0.494,0.499,0.4997,0.495,0.494,0.494]
dry_pixel = [0.494,0.494,0.494,0.494,0.494,0.494,0.494,0.494,0.494,0.494]

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

I_refs = np.loadtxt('dry.txt', delimiter=' ', comments='#').flatten()
dB_refs = np.repeat(dB_ref[0], len(I_refs))
for i in range(dry_time-1):
    # get data
    I_smps = np.loadtxt('wet' + str(i+1) + '.txt', delimiter=' ', comments='#').flatten()
    dB_smps = np.repeat(dB_smp[i], len(I_smps))

    # dH20 mean
    dH20 = np.mean(calculate_dH20(I_refs, I_smps, dB_refs, dB_smps))
    dH20_std = np.std(calculate_dH20(I_refs, I_smps, dB_refs, dB_smps))
    dH20s.append(dH20)
    dH20_stds.append(dH20_std)

dH20s.append(0)
dH20_stds.append(0)
print(dH20s)
print(dH20_stds)

# # RWC with THz
# dH20 = calculate_dH20(I_ref, I_smp, dB_ref, dB_smp)
dH20 = dH20s
RWC_THz = dH20/dH20[0] * 100
RWC_THz_std = dH20_stds/dH20[0] * 100

# RWC with gravimetric balance
RWC_gravimetric = (wet_weight - dry_weight) / (wet_weight[0] - dry_weight) * 100

plt.subplot(2, 1, 1)
plt.scatter(time, RWC_gravimetric, label='Gravimetric', color='black')
plt.errorbar(time, RWC_THz, yerr=np.array(RWC_THz_std), color='green')  # Fix: Convert RWC_THz_std to a numpy array
plt.scatter(time, RWC_THz, label='THz', color='green')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('RWC vs Time')
plt.legend()
plt.tight_layout()
# plt.show()

plt.subplot(2, 1, 2)
plt.scatter(time, dH20, label='dH20', color='red')
plt.xlabel('Time')
plt.ylabel('d_H20')
plt.title('d_H20 vs Time')
plt.legend()
plt.tight_layout()
plt.show()
