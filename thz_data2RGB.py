import numpy as np
from terasense.worker import Worker
import cv2
import terasense.processor as processor
import matplotlib.pyplot as plt

# load data by txt
# data = np.loadtxt('thz_data_API.txt')

# load real-time data
proc = processor.processor(threaded=False)
data = proc.read()

print("Data type:", data.dtype)
print("Data shape:", data.shape)
print("Max value:", data.max())
print("Min value:", data.min())

worker = Worker(size=(32, 32), flags=Worker.DEFAULT_FLAGS)

print(data)
# Convert data to 8-bit unsigned integer
# data_8bit = (data - data.min()) / (data.max() - data.min()) * 255
data_8bit = data*255
data_8bit = data_8bit.astype(np.uint8)

rgb_img = worker.data2RGB(data_8bit)


plt.subplot(1, 3, 1)
plt.imshow(data_8bit, cmap='gray')
plt.axis('off')
plt.title('8-bit Data Gray')

plt.subplot(1, 3, 2)
plt.imshow(data_8bit, cmap='jet')
plt.axis('off')
plt.title('8-bit Data Jet')

plt.subplot(1, 3, 3)
plt.imshow(rgb_img)
plt.axis('off')
plt.title('RGB Image')

plt.show()