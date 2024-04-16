# Description
The overall aim of this project is to demonstrate the feasibility of measuring water status in ryegrass non-destructively using THz spectroscopy.

Data: THz spectroscopy measurements of ryegrass. 
Desired Output: 
* THz spectroscopy measurements of a large variety of ryegrass plants with different morphology and genotype. 
* Code-based automated analysis of the acquired data with insight into reproducibility and uncertainty analysis. 

# File docs
thz_XXXX.py: scripts that require THz camera and THz source API

## Data fetching & Processing
* thz_get_data.py: save pixel value data file
* thz_get_img.py: save pixel value img and data file
* thz_plot_atnu_pix.py: plot pixel_avrg vs atnu(0~40)
* thz_atnu_pix_fit.py: fit the pixel_avrg vs atnu plot with intensity equasion
* img_plants_0dB: img of plants in 0 dB
* test_imgs: img of test pixel plots(for the rotation problem)
* plot_pix_atnu: plot of pix against atnu

## Water penetration layer expr
* thz_wtrexpr_getAPIdata.py: save water expr API data to water_layer_expr_API
* wtrexpr_alpha.py: calculate dH20 based on data from water_layer_expr_API and plot the result
* water_layer_expr_API: pixel value and atnu data acquire form API
* (not in use)wtrexpr_equation_sftw.py: calculate dH20 based on data from water_layer_expr and plot the result
* (not in use)water_layer_expr: pixel value and atnu data acquire form software

## Leaf penetration expr
* thz_leafexpr_selectpix.py: select working area and save the index in leaf_expr_API/working_index.txt
* thz_leafexpr_getAPIdata.py: save leaf expr API data to leaf_expr_API
* leafexpr_dH20.py: calculate dH20, RWC_gravimetric, RWC_THz and make plots using the data from leaf_expr_API
* leaf_expxr_API: expr data files

## Plant penetration expr
* thz_plantexpr_getAPIdata.py: save plant expr API data to plant_expr_API
* thz_plantexpr_getI0: analyse the threshold range of I0
* plantexpr_dH20.py: calculate avarage attenuation and RWC, and make plots
* plant_expr_API: expr data files