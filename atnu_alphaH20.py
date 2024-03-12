import numpy as np
import matplotlib.pyplot as plt
c0=299792458
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
# Double Debye Model for water from paper https://doi.org/10.1021/jp960141g #
eps_inf=3.48
eps_1=78.36
tau_1=8.24*1e-12
eps_2=4.93
tau_2=0.18*1e-12
########################
freq=np.linspace(0.05,1,1000)*1e12
# Look up parameters at this frequency ####
f_search=0.1*1e12
omega=2*np.pi*freq
eps=eps_inf+(eps_1-eps_2)/(1+1j*tau_1*omega)+(eps_2-eps_inf)/(1+1j*tau_2*omega)
eps_r=np.real(eps)
eps_i=np.imag(eps)
n=np.sqrt((np.sqrt(eps_r**2+eps_i**2)+eps_r)/2)
alpha=((4*np.pi*freq)/c0)*np.sqrt((np.sqrt(eps_r**2+eps_i**2)-eps_r)/2)
fig = plt.figure(1,facecolor="white",figsize=(8,8))
ax0 = fig.add_subplot(211)
ax0.plot(freq/1e9,alpha/100,'-')
ax0.set_ylabel(r'Attenuation (1/cm)')
ax0.set_xlabel(r'Frequency (GHz)')
ax1 = fig.add_subplot(212)
ax1.plot(freq/1e9,n,'-')
ax1.set_ylabel(r'Refractive index')
ax1.set_xlabel(r'Frequency (GHz)')
index=np.where(freq==find_nearest(freq, value=f_search))[0][0]
print(' Attenuation at ' + str(f_search/1e12) +'THz in [1/cm]:',round(alpha[index]/100,2))
print(' Refractive index at ' + str(f_search/1e12) +'THz:',round(n[index],2))