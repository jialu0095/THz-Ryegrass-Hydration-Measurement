import numpy as np

#### Variables:
# Intensity: I
# Attenuation: dB
# Cube Diameter: d
# H20 Absorption Coefficient: alpha_H20

## ref group
# I_ref = 
# dB_ref = 
# d_ref =
 
## smp group
# I_smp = 
# dB_smp =
# d_smp =

# alpha = [ ln(I_ref / I_sample) + 10*ln10 * (dB_ref - dB_smp) ] / d_H20


def calculate_alpha(I_ref, I_sample, dB_ref, dB_smp, d_H2O):
    alpha = (np.log(I_ref / I_sample) + 10*np.log(10) * (dB_ref - dB_smp)) / d_H2O
    return alpha

# alpha = calculate_alpha(I_ref, I_sample, dB_ref, dB_smp, d_H2O)
