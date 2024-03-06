import numpy as np
import os
import matplotlib.pyplot as plt

os.chdir('data_processing')

test_data = np.genfromtxt('data_kiwi_sftw.dat', delimiter=',')
control_data = np.genfromtxt('data_none_sftw.dat', delimiter=',')

fig, ax = plt.subplots(1, 1)
img = ax.imshow(test_data, cmap='jet')
fig.colorbar(img, ax=ax)

print(test_data)
print(test_data.shape)

# np.savetxt('test_frompng.txt', data)
plt.show()

