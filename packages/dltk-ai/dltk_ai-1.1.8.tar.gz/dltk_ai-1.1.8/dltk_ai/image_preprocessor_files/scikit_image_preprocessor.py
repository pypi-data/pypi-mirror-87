# %%
import os
import glob
import numpy as np
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
from skimage import transform, data , color, img_as_float, segmentation, filters
from skimage.transform import rotate, AffineTransform, rescale, resize, downscale_local_mean
from skimage.util import random_noise
from skimage.filters import gaussian
from scipy import ndimage

from skimage.color import (separate_stains, combine_stains,hdx_from_rgb,rgb2xyz,rgb2gray, rgb_from_hdx,gray2rgb, convert_colorspace)

from skimage.restoration import (denoise_tv_chambolle, denoise_bilateral,denoise_wavelet, estimate_sigma)


from skimage.morphology import erosion, dilation, opening, closing, white_tophat
#%%
def extract_images(folder_path):
  data_path = os.path.join(folder_path,'*g') 
  files = glob.glob(data_path) 
  imgfiles=[]
  for files in files:
    if (files.endswith(".jpeg")==True)|(files.endswith(".jpg")==True):
      imgfiles.append(files)
  return imgfiles
# %% Transformation
def image_transformation_scikit(image_path,is_image,method,save_image = False):
    # if user selects a invalid method we raise an error
    if method not in ['rotate_clockwise_90','rotate_anticlockwise_90','rotate_180']:
        raise ValueError('Select valid parameter for method- rotate_clockwise_90/rotate_anticlockwise_90/rotate_180')
    if save_image not in [True,False]:
        save_image=False
    # if user inputs single image, check for only image formats and pass for further processing
    if is_image == True:
        image = imread(image_path)
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
    #image passes through the mentioned method for transformation 
        if method == 'rotate_clockwise_90':
            rotated_list = rotate(image,90,resize=True)
            if save_image==True:
                imsave('image_rotate_clockwise_90.jpg', rotated_list)
            
        elif method == 'rotate_anticlockwise_90':
            rotated_list = rotate(image,270,resize=True)
            if save_image==True:
                imsave('image_rotate_anti_clockwise_90.jpg', rotated_list)
       
        elif method == 'rotate_180':
            rotated_list = rotate(image,180,resize=True)
          #save_image= True will save the image file to the woring directory to view   
            if save_image==True:
                imsave('image_rotate_anti_clockwise_90.jpg', rotated_list)
    #if is_image== False, loop continuous to process and check for only image format files for further processing
    elif is_image == False:
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: pass
        #creating new list to append all the processed content into rotated_list=[]
        rotated_list= []
        #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        image_count= 1
        image_path_list = extract_images(image_path)
        for i in image_path_list:
            image_read = imread(i)
        ##image passes through the mentioned method for transformation   
            if method == 'rotate_clockwise_90':
                #rotated = rotate(image_read,method=90)
                rotated = rotate(image_read, 90, resize=True)
                if save_image==True:
                    imsave('image_{}_resize-rotate_clockwise_90.jpg'.format(image_count), rotated)
                    print('saved')
                rotated_list.append(rotated)
            elif method == 'rotate_anticlockwise_90':
                rotatedacc = rotate(image_read,270,resize=True)
                if save_image==True:
                    imsave('image_{}_resize-rotate_anticlockwise_90.jpg'.format(image_count), rotatedacc)
                    print('saved')
                rotated_list.append(rotatedacc)
            elif method == 'rotate_180':
                rotatedoo = rotate(image_path,180,resize=True)
                if save_image==True:
                    imsave('image_{}_resize-rotate_180.jpg'.format(image_count), rotatedoo)
                    print('saved')
                rotated_list.append(rotatedoo)
            else:
                print('wrong')
         #image_count gets incrimented everytime a new file gets processed.       
            image_count+=1
   #retrning the appended list of processed image data
    return rotated_list
#%%
#image_transformation_scikit('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,'rotate_clockwise_90',True)

# %%
#colorspace
#colorspace
def image_colorspace_scikit(image_path,is_image,method,save_image=False):
  # if user selects a invalid method we raise an error and default save image to False is the used provides codition other than true / false.
    if method not in ['red','green','yellow','grey','blue']:
        raise ValueError('choose color in red/green/yellow/grey/blue')
    if save_image not in [True,False]:
        save_image=False
    # if user inputs single image, check for only image formats and pass for further processing
    if is_image == True:
        image = imread(image_path)
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
      #image passes through the mentioned method for color change and for every save_image= True image saves.
        if method == 'red':
            red_multiplier = [1, 0, 0]
            color_list = red_multiplier * image
            if save_image==True:
                imsave('image_red.jpg', color_list)
        elif method =='green':
            green_multiplier= [0,1,0]
            color_list = green_multiplier* image
            if save_image==True:
                imsave('image_green.jpg', color_list)
        elif method == 'yellow':
            yellow_multiplier= [1,1,0]
            color_list= yellow_multiplier*image
            if save_image==True:
                imsave('image_yellow.jpg', color_list)
        elif method == 'grey':
            color_list = rgb2gray(image)
            if save_image==True:
                imsave('image_grey.jpg', color_list)
        elif method == 'blue':
            blue_multiplier = [0,0,1]
            color_list= blue_multiplier*image
            if save_image==True:
                imsave('image_blue.jpg', color_list)  
  #if is_image== False, loop continuous to process and check for only image format files for further processing          
    elif is_image == False:
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: pass
     #creating new list to append all the processed content into color_list=[]   
        color_list= []
     #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        image_count=1
     #extract_images function gets activated and images are read and stored into image_path_list
        image_path_list = extract_images(image_path)
        for i in image_path_list:
            image_read = imread(i)
     #image passes through the mentioned method for color change
            if method == 'red':
                red_multiplier = [1, 0, 0]
                rdata = red_multiplier * image_read
                if save_image==True:
                    imsave('image_{}_color_red.jpg'.format(image_count), rdata)
                    print('saved')
                color_list.append(rdata)
            elif method =='green':
                green_multiplier= [0,1,0]
                gdata = green_multiplier* image_read
                if save_image==True:
                    imsave('image_{}_color_green.jpg'.format(image_count), gdata)
                    print('saved')
                color_list.append(gdata)
            elif method== 'yellow':
                yellow_multiplier= [1,1,0]
                ydata= yellow_multiplier*image_read
                if save_image==True:
                    imsave('image_{}_color_yellow.jpg'.format(image_count), ydata)
                    print('saved')
                color_list.append(ydata)
            elif method == 'grey':
                color_list = rgb2gray(image_read)
                if save_image==True:
                    imsave('image_{}_color_grey.jpg'.format(image_count), color_list)
            elif method == 'blue':
                blue_multiplier = [0,0,1]
                color_list= blue_multiplier*image_read
                if save_image==True:
                    imsave('image_{}_color_blue.jpg'.format(image_count), color_list)   
            else:
                print('wrong input operation')
            print(image_count)
        #image_count gets incrimented everytime a new file gets processed.
            image_count+=1
   #retrning the appended list of processed image data
    return color_list
#%%
#image_colorspace_scikit('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data',False,'red',True)
#%%
# resize
def image_resize_scikit(image_path,is_image,method,save_image=False):
    # if user selects a invalid method we raise an error
    if method not in['stretch_vertical', 'stretch_horizontal','resize_small']: raise ValueError('Please input correct method. Valid inputs: ''stretch_vertical', 'stretch_horizontal','resize_small')  
    # if user inputs single image, check for only image formats and pass for further processing
    if is_image == True:
        image = imread(image_path)
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
    #image passes through the mentioned method for resizing
    #save_image= True will save the image file to the woring directory to view 
        if method == 'stretch_vertical':
            resized_image = resize(image, (image.shape[0] // 2, image.shape[1] // 1), anti_aliasing=True)
            if save_image==True:
                imsave('image_stretch_vertical.jpg', resized_image)
        elif method== 'stretch_horizontal':
            resized_image = resize(image, (image.shape[0] // 2, image.shape[1] // 4), anti_aliasing=True)
            if save_image==True:
                imsave('image_stretch_horizontal.jpg', resized_image)
        elif method == 'resize_small':
            resized_image = resize(image, (image.shape[0] // 1, image.shape[1] // 1), anti_aliasing=True)
            if save_image==True:
                imsave('image_resize_small.jpg', resized_image)
        else:
            print('wrong')
   #if is_image== False, loop continuous to process and check for only image format files for further processing 
    elif is_image == False:
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: pass
        #creating new list to append all the processed content into rotated_list=[]
        resized_image = []
        #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        image_count=1
        #extract_images function gets activated and images are read and stored into image_path_list
        image_path_list = extract_images(image_path)
        for i in image_path_list:
            image_read = imread(i)
            ##image passes through the mentioned method for resizing
            if method == 'stretch_vertical':
                stretch_vertical = resize(image_read, (image_read.shape[0] // 2, image_read.shape[1] // 1), anti_aliasing=True)
                if save_image==True:
                    imsave('image_{}_stretch_vertical.jpg'.format(image_count),stretch_vertical)
                    print('saved')
                resized_image.append(stretch_vertical)
            elif method== 'stretch_horizontal':
                stretch_hori = resize(image_read, (image_read.shape[0] // 2, image_read.shape[1] // 4), anti_aliasing=True)
                if save_image==True:
                    imsave('image_{}_stretch_horizontal.jpg'.format(image_count),stretch_hori)
                    print('saved')
                resized_image.append(stretch_hori)
            elif method == 'resize_small':
                resize_small = resize(image_read, (image_read.shape[0] // 1, image_read.shape[1] // 1), anti_aliasing=True)
                if save_image==True:
                    imsave('image_{}_resize_small.jpg'.format(image_count),resize_small)
                    print('saved')
                resized_image.append(resize_small)
            #image_count gets incrimented everytime a new file gets processed.
            image_count+=1
    print(resized_image)
    #retrning the appended list of processed image data        
    return resized_image
#%%
#image_resize_scikit('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,'stretch_vertical',False)



# %%
#smoothing
#smoothing
def image_smoothing_scikit(image_path,is_image,method,save_image=False):
  # if user selects a invalid method we raise an error
    if method not in['denoise_tv_chambolle','denoise_bilateral','denoise_wavelet']: raise ValueError('Please input correct Operation. Valid inputs: ''denoise_tv_chambolle','denoise_bilateral','denoise_wavelet')  
    # if user inputs single image, check for only image formats and pass for further processing
    if is_image == True:
        image = imread(image_path)
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
        #standard scikit, skimage.restoration module values and fnctions used
        sigma = 0.155
        noisy = random_noise(image, var=sigma**2)
        sigma_est = estimate_sigma(noisy, multichannel=True, average_sigmas=True)
        #image passes through the mentioned method for SMOOTHING
        #save_image= True will save the image file to the woring directory to view 
        if method == 'denoise_tv_chambolle':
            smooth_list = denoise_tv_chambolle(noisy, weight=0.1, multichannel=True)
            if save_image==True:
                imsave('image_denoise_tv_chambolle.jpg', smooth_list)
      
        elif method == 'denoise_bilateral':
            print('entered denoise_bilateral')
            smooth_list = denoise_bilateral(noisy, sigma_color=0.1, sigma_spatial=15, multichannel=True)
            if save_image==True:
                imsave('image_denoise_bilateral.jpg', smooth_list)
      
        elif method == 'denoise_wavelet':
            smooth_list= denoise_wavelet(noisy, multichannel=True, convert2ycbcr=True, rescale_sigma=True)
            if save_image==True:
                imsave('image_denoise_wavelet.jpg', smooth_list)
   #if is_image== False, loop continuous to process and check for only image format files for further processing   
    elif is_image == False:
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: pass
        #creating new list to append all the processed content into rotated_list=[]
        smooth_list = []
        #extract_images function gets activated and images are read and stored into image_path_list
        image_path_list = extract_images(image_path)
        #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        image_count = 1
        for i in image_path_list:
            image_read = imread(i)
            sigma = 0.155
            noisy = random_noise(image_read, var=sigma**2)
            sigma_est = estimate_sigma(noisy, multichannel=True, average_sigmas=True)
            #image passes through the mentioned method for smoothing 
            if method == 'denoise_tv_chambolle':
                dn1= denoise_tv_chambolle(noisy, weight=0.1, multichannel=True)
                if save_image==True:
                    imsave('image_{}_denoise_tv_chambolle.jpg'.format(image_count), dn1)
                    print('saved')
                smooth_list.append(dn1)
            elif method == 'denoise_bilateral':
                print('entered denoise_bilateral')
                dnbill2 = denoise_bilateral(noisy, sigma_color=0.1, sigma_spatial=15, multichannel=True)
                if save_image==True:
                    imsave('image_{}_denoise_bilateral.jpg'.format(image_count),dnbill2)
                    print('saved')
                smooth_list.append(dnbill2)
            elif method == 'denoise_wavelet':
                dnwave2= denoise_wavelet(noisy, multichannel=True, convert2ycbcr=True, rescale_sigma=True)
                if save_image==True:
                    imsave('image_{}_denoise_wavelet.jpg'.format(image_count),dnwave2)
                    print('saved')
                smooth_list.append(dnwave2)
            #image_count gets incrimented everytime a new file gets processed.
            image_count+=1
     #retrning the appended list of processed image data
    return smooth_list

# %%
#image_smoothing_scikit('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data',False,'denoise_wavelet',True)

# %% morphology
# %% morphology
def image_morphology_scikit(image_path,is_image,method,save_image=False):
  # if user selects a invalid method we raise an error
    if method not in['erosion','dilation']: 
         raise ValueError('Please input correct Operation. Valid inputs:''erosion','dilation')
    # if user inputs single image, check for only image formats and pass for further processing.
    #save_image= True will save the image file to the woring directory to view 
    if is_image == True:
        image = imread(image_path)
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
        #image passes through the mentioned method for morphology 
        if method == 'erosion':
            morph_list = erosion(image, selem=None, out=None)
            if save_image==True:
                imsave('image_erosion.jpg', morph_list)
        elif method == 'dilation':
            morph_list = dilation(image, selem=None, out=None)
        if save_image==True:
            imsave('image_dilation.jpg', morph_list)
    #if is_image== False, loop continuous to process and check for only image format files for further processing
    elif is_image == False:
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: pass
        #creating new list to append all the processed content into morph_list=[]
        morph_list = []
        #extract_images function gets activated and images are read and stored into image_path_list
        image_path_list = extract_images(image_path)
        #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        image_count = 1
        for i in image_path_list:
            image_read = imread(i)
            #image passes through the mentioned method for morphology
            if method == 'erosion':
                err = erosion(image_read, selem=None, out=None)
                if save_image==True:
                    imsave('image_{}_erosion.jpg'.format(image_count),err)
                    print('saved')
                morph_list.append(err) 
            elif method == 'dilation':
                dilate = dilation(image_read, selem=None, out=None)
                if save_image==True:
                    imsave('image_{}_dilasion.jpg'.format(image_count),dilate)
                    print('saved')
                morph_list.append(dilate)
            else:
                print('wrong operation')
            #image_count gets incrimented everytime a new file gets processed.
            image_count+=1
    #retrning the appended list of processed image data        
    return morph_list
#%%
#image_morphology_scikit('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data',False,'dilation',True)
# %%
def image_segmentation_scikit(image_path, is_image,save_image=False):
  # if user inputs single image, check for only image formats and pass for further processing
  #image passes through the mentioned method for segmentation 
  #save_image= True will save the image file to the woring directory to view 
    if is_image == True:
        #image = imread(image_path)
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
        image_read = imread(image_path)
        image_read = rgb2gray(image_read)
        mask = image_read > filters.threshold_otsu(image_read)
        clean_border = segmentation.clear_border(mask).astype(np.int)
        seg_edges = segmentation.mark_boundaries(image_read, clean_border)
        if save_image==True:
            imsave('image_segmentation.jpg', seg_edges)
        edges=seg_edges
    #if is_image== False, loop continuous to process and check for only image format files for further processing
    elif is_image == False:
        if (image_path.endswith('.jpeg') or image_path.endswith('.png') or image_path.endswith('.jpg')): pass
        else: pass
        #creating new list to append all the processed content into edges=[]
        edges = []
        #extract_images function gets activated and images are read and stored into image_path_list
        image_path_list = extract_images(image_path)
        #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        image_count = 1
        #image passes through the mentioned method for segmentation
        #save_image= True will save the image file to the woring directory to view 
        for i in image_path_list:
            image_read = imread(i)
            image_read = rgb2gray(image_read)
            mask = image_read > filters.threshold_otsu(image_read)
            clean_border = segmentation.clear_border(mask).astype(np.int) 
            seg_edges = segmentation.mark_boundaries(image_read, clean_border)
            if save_image==True:
                imsave('image_{}_segmentation.jpg'.format(image_count),seg_edges)
                print('saved')
            edges.append(seg_edges)
            image_count+=1
    return edges
#%%
#image_segmentation_scikit('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,True)

# %%
