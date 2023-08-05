from dltk_ai.image_preprocessor_files.opencv_preprocessor import *
from dltk_ai.image_preprocessor_files.scikit_image_preprocessor import *
import warnings

def image_transformation(datapath,is_image,method,library,save_image=False,show_image=False):
    if library == 'opencv':
        transformed = image_transformation_opencv(datapath=datapath,is_image=is_image,method=method,save_image=save_image,show_image=False)
    if library == 'scikit_image':
         if show_image==True:
             warnings.warn('there is no show_image feature for scikit_image. defaulting show_image to False')
         transformed = image_transformation_scikit(image_path=datapath,is_image=is_image,method=method,save_image=save_image)
    return transformed

def image_colorspace(datapath,is_image,method,library,save_image=False,show_image=True):
    if library=='opencv':
        r_color = image_colorspace_opencv(datapath=datapath, is_image=is_image, method=method, show_image=show_image,save_image=save_image)
        if show_image == True:
            warnings.warn('there is no show_image feature for scikit_image. defaulting show_image to False')
    if library == 'scikit_image':
        r_color = image_colorspace_scikit(image_path=datapath,is_image=is_image,method=method,save_image=save_image)
    return r_color

def image_resize(datapath,is_image, method, library, save_image=False, show_image= False,width=None,height=None):
    if library== 'opencv':
        r_resize= image_resize_opencv(datapath= datapath,is_image= is_image ,method= method,show_image=show_image, save_image= save_image,width= width, height= height)
    if library == 'scikit_image':
        if show_image== True:
            warnings.warn('There is no show_image feature for scikit_image. defaulting show_image to False')
        r_resize= image_resize_scikit(image_path= datapath,is_image= is_image ,method= method, save_image= save_image)
    return r_resize

def image_segmentation(datapath,is_image,library, save_image=False, show_image= False):
    if library== 'opencv':
        r_segmentaton= image_segmentation_opencv(datapath= datapath,is_image= is_image,show_image=show_image, save_image= save_image )
    if library == 'scikit_image':
        if show_image== True:
            warnings.warn('There is no show_image feature for scikit_image. defaulting show_image to False')
        r_segmentaton= image_segmentation_scikit(image_path = datapath,is_image= is_image, save_image= save_image)
    return r_segmentaton

def image_smoothing(datapath,is_image, method, library, save_image=False, show_image= False):
    if library== 'opencv':
        r_smoothing= image_smoothing_opencv(datapath= datapath,is_image=is_image,method=method,show_image=show_image, save_image= save_image )
    if library == 'scikit_image':
        if show_image== True:
            warnings.warn('There is no show_image feature for scikit_image. defaulting show_image to False')
        r_smoothing = image_smoothing_scikit(image_path= datapath,is_image= is_image, method=method,save_image= save_image)
    return r_smoothing

def image_morphology(datapath,is_image, method, library, save_image=False, show_image= False):
    r_morphology=[]
    if library== 'opencv':
        r_morphology= image_morphology_opencv(datapath= datapath,is_image=is_image,method=method,show_image=show_image, save_image= save_image )
    if library == 'scikit_image':
        if show_image== True:
            warnings.warn('There is no show_image feature for scikit_image. defaulting show_image to False')
        r_morphology= image_morphology_scikit(image_path= datapath,is_image= is_image, method=method,save_image= save_image)
    return r_morphology

if __name__ == '__main__':
    print("hello")

    a= image_morphology(r'C:\Users\Gowtham\Desktop\rohith\dog.jpg',True,'dilation','scikit_image',True)
    print(a)
