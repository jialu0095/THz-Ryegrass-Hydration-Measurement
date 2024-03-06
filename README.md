The overall aim of this project is to demonstrate the feasibility of measuring water 
status in ryegrass non-destructively using THz spectroscopy.

Data: 
THz spectroscopy measurements of ryegrass. 
Desired Output: 
a) THz spectroscopy measurements of a large variety of ryegrass plants with 
different morphology and genotype. 
b) Code-based automated analysis of the acquired data with insight into 
reproducibility and uncertainty analysis. 

Naming: thz_data/script

thz_ python scripts:
    data2RGB: monologue RGB data with one-channel data(read from API)
    img_process: same as data2RGB but on sftw data files    
    
    get_img: read data from the camera and store data file and img(gray-scale, jet)
    source_adjust: adjust attenuation
    combine_atnu_img: script that will auto-adjust attenuation based on the pixels
    plot_atnu_pix: plot the relationships btw attenuation and pixel value