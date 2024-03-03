# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import numpy as np
# import scipy.ndimage as ndimage
# plt.close('all')
# #img=mpimg.imread('kiwi mark II (large).png')
# #imgplot = plt.imshow(img)
# background=np.loadtxt('background.dat',delimiter=',')
# image_raw = np.loadtxt('grass_plant_a.dat',delimiter=',')
# fig = plt.figure(1)
# plt.imshow(background)  #, interpolation='nearest'
# fig = plt.figure(2)
# plt.imshow(image_raw)  #, interpolation='nearest'
# plt.show()
# #background=np.abs(np.random.random((32,32)))*0.5
# image_corr=image_raw/background
# #imgplot = plt.imshow(image_corr)
# #image_corr = ndimage.gaussian_filter(image_corr, sigma=(1, 1), order=0)
# fig = plt.figure(3)
# plt.imshow(image_corr)  #, interpolation='nearest'
# plt.show()
# #alpha=10
# #d=(1/alpha)*np.log(1/image_corr)
# #plt.imshow(d)
# #plt.show()


import numpy as np
import matplotlib.pyplot as plt
from terasense import processor

def save_image(data, filename='terahertz_image.png'):
    """Save the numpy array data as an image."""
    plt.imshow(data, cmap='gray')  # Display the data as a gray-scale image
    plt.colorbar()  # Add a color bar to indicate the scale
    plt.savefig(filename)  # Save the figure to a file
    plt.close()  # Close the figure to free up memory

def main():
    # Initialize an instance of the processor class with default settings
    proc = processor.processor(threaded=True)

    try:
        # Define a simple callback function to handle the acquired data
        def data_callback(data):
            print("Data acquired")
            save_image(data, filename='terahertz_image.png')

        # Start data acquisition and processing, using data_callback as the callback
        proc.start(callback=data_callback)

        # Wait enough time to acquire and process data
        # Note: The sleep time may need to be adjusted based on your specific device and setup
        input("Press Enter to stop acquisition...")

    finally:
        # Stop data acquisition and processing, ensuring resources are properly cleaned up
        proc.stop(join=True)

if __name__ == '__main__':
    main()
