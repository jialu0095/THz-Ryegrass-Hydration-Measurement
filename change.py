#%%
import pandas as pd
import numpy as np

# 读取 CSV 文件
df = pd.read_csv('dB_wet2_One50_3.csv')

# 减去 1.2
df[df!=0] -= 0.3
# 将所有小于0的值变为0
df[df < 0] = 0

# 保留小数点后一位

df = df.round(1)


# 输出到新的 CSV 文件
df.to_csv('modified_dB_wet2_One50_3.csv', index=False)


# 读取 CSV 文件
df = pd.read_csv('dB_wet5_One50_3.csv')

# 减去 1.2
df[df!=0] -= 0.3
# 将所有小于0的值变为0
df[df < 0] = 0

# 保留小数点后一位

df = df.round(1)


# 输出到新的 CSV 文件
df.to_csv('modified_dB_wet5_One50_3.csv', index=False)
# %%
