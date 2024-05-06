#%%
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans

# change working dir
os.chdir('plant_expr_API')
print(os.getcwd())

#%%
I_0s = np.loadtxt('I_0s_dry.txt', delimiter=' ', comments='#').flatten()
# I_0s = np.loadtxt('I_0s_empty.txt', delimiter=' ', comments='#').flatten()
I_0s = np.loadtxt('I_0s_wet.txt', delimiter=' ', comments='#').flatten()
not_negative_one_index = I_0s != -1
I_0s = I_0s[not_negative_one_index]
# KMeans clustering
k = 5 
kmeans = KMeans(n_clusters=k)
clusters = kmeans.fit_predict(I_0s.reshape(-1, 1))

# cluster labels
# print("Cluster Labels:", clusters)

#%%
print('mean: ', np.mean(I_0s))
print('std: ', np.std(I_0s)) 
print('lower quantile: ', np.quantile(I_0s, 0.25))
print('higher quantile: ', np.quantile(I_0s, 0.75))
print('min: ', np.min(I_0s))
print('max: ', np.max(I_0s))
#%%
# Plot
x = np.arange(len(I_0s))
plt.scatter(x, I_0s, c=clusters, cmap='coolwarm')
plt.xlabel('Pixels')
plt.ylabel('I_0s')
plt.title('Wet Leaf I_0')
plt.show()


# %%
