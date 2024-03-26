import numpy as np
import numpy as np

def calculate_dH20(I_ref, I_smp, dB_ref, dB_smp):
    I_ref = np.array(I_ref)
    I_smp = np.array(I_smp)
    dB_ref = np.array(dB_ref)
    dB_smp = np.array(dB_smp)
    
    d_H20 = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / 85
    return d_H20

time = [1,2,3,4,5]

I_smp = [0.477,0.477,0.477,0.477,0.477]
dB_smp = [5.8,5.8,5.8,5.8,5.8]
I_ref = [0.483,0.494,0.462,0.495,0.468]
dB_ref = [5.8,5.0,5.4,5.0,5.4]



dH20 = calculate_dH20(I_ref, I_smp, dB_ref, dB_smp)

import matplotlib.pyplot as plt

plt.plot(time, dH20)
plt.xlabel('Time')
plt.ylabel('dH20')
plt.title('dH20 vs Time')
plt.show()

print(dH20)