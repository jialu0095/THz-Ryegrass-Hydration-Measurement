import numpy as np
from terasense import processor


proc = processor.processor(threaded=False)

# time used to get 1/32 frame (usec)
data=proc.read()
print(proc.GetIntTime())

# save bg data
thz_bg_data = proc.read()
print(thz_bg_data)
np.savetxt('thz_bg_data.txt', data, fmt='%f')

