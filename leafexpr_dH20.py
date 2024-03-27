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
dry_time = 7
for i in range(dry_time):
    time.append(i+1)

# expr data
wet_weight = [0.6833,0.6383,0.6236,0.6143,0.6050,0.5953,0.5861]
dry_weight = [0.5763,0.5763,0.5763,0.5763,0.5763,0.5763,0.5763]

wet_attenuation = [3.4,3.4,3.4,3.8,3.8,4.2,4.2]
dry_attenuation = [4.2,4.2,4.2,4.2,4.2,4.2,4.2]

wet_pixel = [0.485,0.477,0.492,0.475,0.478,0.473,0.479]
dry_pixel = [0.479,0.479,0.479,0.479,0.479,0.479,0.479]

# expr variables
fresh_weight = 0.6833
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
plt.subplot(2, 1, 1)
plt.scatter(time, RWC_gravimetric, label='Gravimetric')
plt.xlabel('Time')
plt.ylabel('RWC (%)')
plt.title('RWC vs Time')
plt.legend()

plt.subplot(2, 1, 2)
plt.scatter(time, RWC_THz, label='dH20')
plt.xlabel('Time')
plt.ylabel('dH20')
plt.title('dH20 vs Time')
plt.legend()

plt.tight_layout()
plt.show()

