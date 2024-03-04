import numpy as np
import matplotlib.pyplot as plt
from terasense import processor

def save_image(data, filename='terahertz_image.png', rotate=True, mirror=False):
    """Save the numpy array data as an image with optional rotate and mirror."""
    if rotate:
        data = np.rot90(data)  # Rotate the image (90 degrees)
    if mirror:
        data = np.fliplr(data)  # Mirror the image horizontally
    plt.imshow(data, cmap='viridis')  # Display the data as a pesudo color img
    plt.imshow(data, cmap='grey')  # Display the data as a grey scale img
    plt.colorbar()  # Add a color bar to indicate the scale
    plt.savefig(filename)  # Save the figure to a file
    plt.close()  # Close the figure to free up memory

def save_data_to_npy(data, filename='thz_data.npy'):
    """Save the numpy array data to a npy file."""
    np.save(filename, data) 

def save_data_to_txt(data, filename='thz_data.txt'):
    """Save the numpy array data to a text file."""
    np.savetxt(filename, data, fmt='%f')  # You can change the format specifier if needed



def main():
    # Initialize an instance of the processor class in single-threaded mode
    proc = processor.processor(threaded=False)

    try:
        # Start data acquisition without threading
        data = proc.read()  # This call will block until data is available
        if data is not None:
            print("Data acquired")
            print("Data type:", data.dtype)
            print("Data shape:", data.shape)
            print("Max value:", data.max())
            print("Min value:", data.min())
            # save_image(data, filename='thz_img_viridis.png')
            save_image(data, filename='thz_img_grey_book.png')
            # save_data_to_npy(data, filename='thz_data.npy')
            save_data_to_txt(data, filename='thz_data_book.txt')
        else:
            print("No data was read. Check the camera connection and settings.")
    
        print("Data acquired")

    finally:
        # Perform any necessary cleanup here
        pass

if __name__ == '__main__':
    main()
