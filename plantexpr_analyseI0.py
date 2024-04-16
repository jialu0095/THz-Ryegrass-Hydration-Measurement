#%%
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans

# change working dir
os.chdir('plant_expr_API')
print(os.getcwd())

#%%
I_0s = np.loadtxt('I_0s_empty.txt', delimiter=' ', comments='#').flatten()
# KMeans clustering
k = 5 
kmeans = KMeans(n_clusters=k)
clusters = kmeans.fit_predict(I_0s.reshape(-1, 1))

# cluster labels
print("Cluster Labels:", clusters)

#%%
# Plot
plt.scatter(x, I_0s, c=clusters, cmap='coolwarm')
plt.xlabel('Index')
plt.ylabel('I_0s')
plt.title('Outliers of I_0s')
plt.show()

#%%
print('mean: ', np.mean(I_0s))
print('std: ', np.std(I_0s)) 
print('lower quantile: ', np.quantile(I_0s, 0.25))
print('higher quantile: ', np.quantile(I_0s, 0.75))
# %%
