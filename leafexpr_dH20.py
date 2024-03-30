import numpy as np
import numpy as np
import matplotlib.pyplot as plt

def calculate_dH20(I_ref, I_smp, dB_ref, dB_smp):
    I_ref = np.array(I_ref)
    I_smp = np.array(I_smp)
    dB_ref = np.array(dB_ref)
    dB_smp = np.array(dB_smp)
    
    d_H20 = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / 85
    return d_H20

time = []
dry_time = 10
for i in range(dry_time):
    time.append(i+1)

# expr data
wet_weight = [0.9313,0.9080,0.8865,0.8670,0.8470,0.8225,0.8035,0.7835,0.7676,0.7540]
dry_weight = [0.6510,0.6510,0.6510,0.6510,0.6510,0.6510,0.6510,0.6510,0.6510,0.6510]

wet_attenuation = [1.6,1.6,1.8,1.8,2.1,2.1,2.2,2.4,2.5,2.4]
dry_attenuation = [3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2]

wet_pixel = [0.498,0.494,0.474,0.496,0.494,0.499,0.4997,0.495,0.494,0.499]
dry_pixel = [0.496,0.496,0.496,0.496,0.496,0.496,0.496,0.496,0.496,0.496]

# expr variables
fresh_weight = 0.9192
wet_weight = np.array(wet_weight)
dry_weight = np.array(dry_weight)

I_smp = wet_pixel
dB_smp = wet_attenuation
I_ref = dry_pixel
dB_ref = dry_attenuation

# RWC with THz
dH20 = calculate_dH20(I_ref, I_smp, dB_ref, dB_smp)
RWC_THz = dH20/dH20[0] * 100

# RWC with gravimetric balance
RWC_gravimetric = (wet_weight - dry_weight) / (fresh_weight - dry_weight) * 100

print(time)
print(RWC_gravimetric)
print(dH20)

# plots
# plt.subplot(2, 1, 1)
# plt.scatter(time, RWC_gravimetric, label='Gravimetric')
# plt.xlabel('Time')
# plt.ylabel('RWC (%)')
# plt.title('RWC vs Time')
# plt.legend()

# plt.subplot(2, 1, 2)
# plt.scatter(time, RWC_THz, label='dH20')
# plt.xlabel('Time')
# plt.ylabel('dH20')
# plt.title('dH20 vs Time')
# plt.legend()
# plt.figure()

plt.scatter(time, RWC_gravimetric, label='Gravimetric', color='black')
plt.scatter(time, RWC_THz, label='THz', color='green')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('RWC vs Time')
plt.legend()
plt.tight_layout()
plt.show()

# std for error bars
# std_dev_gravimetric = np.std(RWC_gravimetric)
# std_dev_THz = np.std(RWC_THz)

# print(std_dev_gravimetric)
# print(std_dev_THz)

# plt.errorbar(time, RWC_gravimetric, yerr=std_dev_gravimetric, fmt='o', label='Gravimetric')
# plt.errorbar(time, RWC_THz, yerr=std_dev_THz, fmt='o', label='dH20')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.title('RWC and dH20 vs Time')
# plt.legend()
# plt.tight_layout()
# plt.show()