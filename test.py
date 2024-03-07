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

# Initialize
proc = processor.processor(threaded=False)
data = proc.read_raw() # get img data