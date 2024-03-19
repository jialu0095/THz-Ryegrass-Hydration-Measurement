# import numpy as np
# from terasense import processor

# # Initialize
# proc = processor.processor(threaded=False)
# # data = proc.read()  # get img data
# data = proc.read_raw()  # get img data

# print("Data type:", data.dtype)
# print("Data shape:", data.shape)
# print("Max value:", data.max())
# print("Min value:", data.min())
# # np.savetxt('thz_data_API_read.txt', data, fmt='%f')
# np.savetxt('thz_data_API_read_raw.txt', data, fmt='%f')

import numpy as np
from terasense import processor

import numpy as np

# 创建一个示例数组
data = np.arange(100).reshape(10, 10)  # 生成一个10x10的数组

# 设定子区域的边界
x_left = 0
x_right = 10
y_top = 0
y_bottom = 10

# 提取子区域
subdata = data[x_left:x_right, y_top:y_bottom]

print(data)
print(subdata)

