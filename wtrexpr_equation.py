#%%
import numpy as np
import os

#%%
# change working dir
os.chdir('water_layer_expr')
print(os.getcwd())

#%%
#### Variables:
# Intensity: I
# Attenuation: dB
# Cube Diameter: d
# H20 Absorption Coefficient: alpha_H20

## ref group
# I_ref = 
# dB_ref = 
 
## smp group
# I_smp = 
# dB_smp =

# alpha = [ ln(I_ref / I_smp) + 0.1*ln10 * (dB_ref - dB_smp) ] / d_H20

def calculate_alpha(I_ref, I_smp, dB_ref, dB_smp, d_H2O):
    alpha = (np.log(I_ref / I_smp) + 0.1*np.log(10) * (dB_ref - dB_smp)) / d_H2O
    return alpha
# alpha = calculate_alpha(I_ref, I_smp, dB_ref, dB_smp, d_H2O)

#%%
def calculate_alpha_batch(ref_file_name, smp_file_name, d_H2O, dB_ref, dB_smp, type='all'):
    ref_data = np.loadtxt(ref_file_name, delimiter=',', comments='#')
    smp_data = np.loadtxt(smp_file_name, delimiter=',', comments='#')

    # de-dimension to 1 dim
    ref_data = ref_data.flatten()
    smp_data = smp_data.flatten()
    ref_data_avrg = np.mean(ref_data)
    smp_data_avrg = np.mean(smp_data)

    if type == 'all':
        I_ref = ref_data
        I_smp = smp_data
    elif type == 'max':
        I_ref = np.max(ref_data)
        I_smp = np.max(smp_data)
    elif type == 'avrg':
        I_ref = ref_data_avrg
        I_smp = smp_data_avrg
    # I_smp = np.sort(I_smp)[-5:]
        
    alpha = calculate_alpha(I_ref, I_smp, dB_ref, dB_smp, d_H2O)
    std_dev = np.std(alpha)

    print(I_ref)
    print(I_smp)
    print(alpha)
    print(np.mean(alpha))
    print(std_dev)

    return alpha

#%%
## 0.02 cuvette
# alpha calculate_alpha_batch('ref_02_dB1606.dat', 'smp_02_dB1390.dat', 0.02, 16.06, 13.90, type='all')
## 0.05 cuvette
alpha = calculate_alpha_batch('ref_05_dB1190.dat', 'smp_05_dB1110.dat', 0.05, 11.90, 11.10, type='all')

# %%
import matplotlib.pyplot as plt
plt.scatter(range(len(alpha)), alpha)
plt.xlabel('Data Point')
plt.ylabel('Alpha')
plt.title('Alpha Values')
plt.show()
# %%

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans

# reshape alpha values to a 2D array
alpha_2d = alpha.reshape(-1, 1)

# number of clusters
n_clusters = 3

# KMeans clustering model
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(alpha_2d)

# cluster labels
labels = kmeans.labels_

#%%
print(labels)
unique_elements, counts = np.unique(labels, return_counts=True)
element_counts = dict(zip(unique_elements, counts))
print(element_counts)


# plot the clustering result
plt.scatter(range(len(alpha)), alpha, c=labels)
plt.xlabel('Data Point')
plt.ylabel('Alpha')
plt.title('Alpha Values with Clustering')
plt.legend()

# fit line
fit_coeffs = np.polyfit(range(len(alpha)), alpha, 1)
fit_line = np.polyval(fit_coeffs, range(len(alpha)))
plt.plot(range(len(alpha)), fit_line, color='red', label='Fit Line')
plt.show()
# %%
