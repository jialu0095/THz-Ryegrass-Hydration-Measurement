#%%
import numpy as np
import os

# change working dir
os.chdir('leaf_expr_API')
print(os.getcwd())

# %%

# %%
working_index = np.loadtxt('working_index.txt', delimiter=' ', comments='#').astype(int)
print(working_index)
# %%
wet_I_title='wet'
print(f'{wet_I_title}.txt')
# %%
