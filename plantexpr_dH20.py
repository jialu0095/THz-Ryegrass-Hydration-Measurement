import os
import numpy as np
import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir('plant_expr_API')

Is = np.loadtxt('wet_I1.txt', delimiter=' ', comments='#')
Is = np.loadtxt('dry_I.txt', delimiter=' ', comments='#')
x_shape = 8
y_shape = 8

# plot the data
Is = Is.reshape((x_shape, y_shape))  # reshape for plot
Is = np.rot90(Is)  
Is = np.rot90(Is)  
Is = np.rot90(Is)
Is = np.fliplr(Is) 


plt.imshow(Is, cmap='jet', vmin=0, vmax=0.6)  # display the data as a pesudo color img
plt.colorbar()
plt.show()

plt.show()