
import cv2
import numpy as np
import glob
import os

# extract images
def extract_images(folder_path):
  data_path = os.path.join(folder_path,'*g') 
  files = glob.glob(data_path) 
  imgfiles=[]
  for files in files:
    if (files.endswith(".jpeg")==True)|(files.endswith(".jpg")==True):
      imgfiles.append(files)
  return imgfiles
#%%
# smoothing
# smoothing
def image_smoothing_opencv(datapath, is_image, method='average', show_image=False,save_image=True):
  # if user selects a invalid method we raise an error
  if method not in['average','gausian_blur','median_blur','bilateral_blur']:
    raise ValueError('Please input correct method. Valid inputs:''average','gausian_blur','median_blur','bilaterial_blur')
  # if user inputs single image, check for only image formats and pass for further processing.
  if is_image== True:
    image = cv2.imread(datapath)
    if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): pass
    else: raise ValueError('please provide a valid image path for is_image=True')
    #image passes through the mentioned method for smoothing 
    #save_image= True will save the image file to the woring directory to view 
    if method== 'average':
      kernel = np.ones((5,5),np.float32)/25
      blurr = cv2.filter2D(image,-1,kernel)
      print('########### {}'.format(blurr))
      if save_image==True:
        cv2.imwrite('image_average.jpg', blurr)
        print('saved')
      smoothing= cv2.imshow('averaging',blurr) if show_image==True else blurr 

    elif method == 'gausian_blur':
      gblur = cv2.GaussianBlur(image,(5,5),0)
      if save_image==True:
        cv2.imwrite('image_gausian_blur.jpg', gblur)
      smoothing =cv2.imshow('gausian blur',gblur)  if show_image==True else gblur

    elif method == 'median_blur':
      mblurr =cv2.medianBlur(image,5)
      if save_image==True:
        cv2.imwrite('image_median_blur.jpg', mblurr)
      smoothing =cv2.imshow('median blur',mblurr)  if show_image==True else mblurr

    elif method== 'bilateral_blur':
      bilateral = cv2.bilateralFilter(image,9,75,75)
      if save_image==True:
        cv2.imwrite('image_bilateral_blur.jpg', bilateral)
      smoothing =cv2.imshow('bilateral blur',bilateral)  if show_image==True else bilateral
  #if is_image== False, loop continuous to process and check for only image format files for further processing
  elif is_image== False:
    if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): raise ValueError('please provide a valid folder path of images for is_image=False')
    else: pass
    #extract_images function gets activated and images are read and stored into image_list
    images_list = extract_images(datapath)
    #creating new list to append all the processed content into rotated_list=[]
    smoothing = []
    image_count = 1
    #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
    for i in images_list:
      image = cv2.imread(i)
      #image passes through the mentioned method for smoothing
      if method== 'average':
        kernel = np.ones((5,5),np.float32)/25
        blurr = cv2.filter2D(image,-1,kernel)
        if save_image==True:
          cv2.imwrite('image_{}_average.jpg'.format(image_count), blurr)
          print('saved')
        smoothing_image= cv2.imshow('averaging',blurr) if show_image==True else blurr 
        smoothing.append(smoothing_image)

      elif method == 'gausian_blur':                      
        gblur = cv2.GaussianBlur(image,(5,5),0)
        if save_image==True:
          cv2.imwrite('image_{}_gausian_blur.jpg'.format(image_count), gblur)
          print('saved')
        smoothing_image =cv2.imshow('gausian blur',gblur)  if show_image==True else gblur
        smoothing.append(smoothing_image)

      elif method == 'median_blur': 
        mblurr =cv2.medianBlur(image,5)
        if save_image==True:
          cv2.imwrite('image_{}_median_blur.jpg'.format(image_count), mblurr)
          print('saved') 
        smoothing_image =cv2.imshow('median blur',mblurr)  if show_image==True else mblurr
        smoothing.append(smoothing_image)

      elif method == 'bilateral_blur':                            
        bilateral = cv2.bilateralFilter(image,9,75,75)
        if save_image==True:
          cv2.imwrite('image_{}_bilateral_blur'.format(image_count),bilateral)
          print('saved')
        smoothing_image =cv2.imshow('bilateral blur',bilateral)  if show_image==True else bilateral
        smoothing.append(smoothing_image)
       #image_count gets incrimented everytime a new file gets processed. 
      image_count+=1  
      #retrning the appended list of processed image data
  return smoothing
#%%
#image_smoothing_opencv('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,'average',True,False)
#%%
# Morphology
def image_morphology_opencv(datapath,is_image,method='erosion', show_image= False,save_image=False):
  # if user selects a invalid method we raise an error
  if method not in['erosion', 'dilation']:
    raise ValueError('Please input correct Operation. Valid inputs:' 'erosion,''dilation')
  # if user inputs single image, check for only image formats and pass for further processing
  if is_image==True:
    image = cv2.imread(datapath)
    if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): pass
    else: raise ValueError('please provide a valid image path for is_image=True')
    #image passes through the mentioned method for morphology
    #save_image= True will save the image file to the woring directory to view 
    if method== 'erosion':
      kernel = np.ones((5,5),np.uint8)
      erosion1 = cv2.erode(image,kernel,iterations = 1)
      if save_image==True:
        cv2.imwrite('erosion_image.jpg', erosion1)
      morphology = cv2.imshow('erosion',erosion1) if show_image==True else erosion1
    elif method == 'dilation':
      kernel = np.ones((5,5),np.uint8)
      dilation = cv2.dilate(image,kernel,iterations = 1)
      if save_image==True:
        cv2.imwrite('dilation_image.jpg', dilation)
      morphology = cv2.imshow('dilation',dilation) if show_image==True else dilation
  #if is_image== False, loop continuous to process and check for only image format files for further processing
  elif is_image== False:
    if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): raise ValueError('please provide a valid folder path of images for is_image=False')
    else: pass
    #extract_images function gets activated and images are read and stored into image_path_list
    images_list = extract_images(datapath)
    #creating new list to append all the processed content into rotated_list=[]
    morphology = []
    #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
    image_count = 1
    for i in images_list:
      image = cv2.imread(i)
      #image passes through the mentioned method for transformation 
      if method== 'erosion':
        kernel = np.ones((5,5),np.uint8)
        erosion1 = cv2.erode(image,kernel,iterations = 1)
        if save_image==True:
          cv2.imwrite('erosion_{}_image.jpg'.format(image_count), erosion1)
        morphology_image = cv2.imshow('erosion',erosion1)if show_image==True else erosion1
        morphology.append(morphology_image)
      elif method == 'dilation':
        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(image,kernel,iterations = 1)
        if save_image==True:
          cv2.imwrite('dilation_{}_image.jpg'.format(image_count), dilation)
        morphology_image = cv2.imshow('dilation',dilation) if show_image==True else dilation
        morphology.append(morphology_image)
      #image_count gets incrimented everytime a new file gets processed.
      image_count+=1
  #retrning the appended list of processed image data
  return morphology
#%%
#image_morphology_opencv('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,'erosion',False,False)
#%%
# Transformation
# Transformation
def image_transformation_opencv(datapath, is_image, method, show_image=False,save_image=False):
  # if user selects a invalid method we raise an error
  if method not in['rotate_anticlockwise_90', 'rotate_clockwise_90','rotate_180']:
    raise ValueError('Please input correct Operation. Valid inputs:''rotate_anticlockwise_90', 'rotate_clockwise_90','rotate_180')
  if save_image not in [True,False]:
      save_image=False  
  # if user inputs single image, check for only image formats and pass for further processing
  if is_image== True:
    image = cv2.imread(datapath)
    if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): pass
    else: raise ValueError('please provide a valid image path for is_image=True')
    #image passes through the mentioned method for transformation
    #save_image= True will save the image file to the woring directory to view  
    if method == 'rotate_clockwise_90':
      img_rotate_90_clockwise = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
      if save_image==True:
        cv2.imwrite('image_rotate_90_clockwise.jpg', img_rotate_90_clockwise)
      transformation = cv2.imshow('rotated_90_clockwise',img_rotate_90_clockwise) if show_image==True else img_rotate_90_clockwise

    elif method == 'rotate_anticlockwise_90':
      img_rotate_90_counterclockwise = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
      if save_image==True:
        cv2.imwrite('image_rotate_90_counterclockwise.jpg', img_rotate_90_counterclockwise)
      transformation =cv2.imshow('rotated_90_counter_clockwise',img_rotate_90_counterclockwise) if show_image==True else img_rotate_90_counterclockwise

    elif method == 'rotate_180':
      img_rotate_180 = cv2.rotate(image, cv2.ROTATE_180)
      if save_image==True:
        cv2.imwrite('image_rotate_180.jpg', img_rotate_180)
      transformation= cv2.imshow('rotated_180',img_rotate_180) if show_image==True else img_rotate_180 
  #if is_image== False, loop continuous to process and check for only image format files for further processing   
  elif is_image== False:

    if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): raise ValueError('please provide a valid folder path of images for is_image=False')
    else: pass
    #extract_images function gets activated and images are read and stored into image_path_list
    images_list = extract_images(datapath)
    #creating new list to append all the processed content into transformation=[]
    transformation= []
    #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
    image_count = 1
    for i in images_list:
      image = cv2.imread(i)
      #image passes through the mentioned method for transformation 
      if method == 'rotate_clockwise_90':
        img_rotate_90_clockwise = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        if save_image==True:
          cv2.imwrite('image_{}_rotate_90_clockwise.jpg'.format(image_count), img_rotate_90_clockwise)
        rotate90 = cv2.imshow('rotated_90_clockwise',img_rotate_90_clockwise) if show_image==True else img_rotate_90_clockwise
        transformation.append(rotate90)

      elif method== 'rotate_anticlockwise_90':
        img_rotate_90_counterclockwise = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if save_image==True:
          cv2.imwrite('image_{}_rotate_90_counterclockwise.jpg'.format(image_count), img_rotate_90_counterclockwise)
        rotate90c =cv2.imshow('rotated_90_counter_clockwise',img_rotate_90_counterclockwise) if show_image==True else img_rotate_90_counterclockwise
        transformation.append(rotate90c)
      elif method == 'rotate_180':
        img_rotate_180 = cv2.rotate(image, cv2.ROTATE_180)
        if save_image==True:
          cv2.imwrite('image_{}_rotate_180.jpg'.format(image_count), img_rotate_180)
          print('saved')
        rotate90ac= cv2.imshow('rotated_180',img_rotate_180) if show_image==True else img_rotate_180 
        transformation.append(rotate90ac)
      #image_count gets incrimented everytime a new file gets processed.
      image_count += 1
  #retrning the appended list of processed image data
  return transformation
#%%
#image_transformation_opencv('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,'rotate_180',False,False)
#%%
def image_colorspace_opencv(datapath, is_image, method='grey', show_image= False,save_image=False):
    # if user selects a invalid method we raise an error
    if method not in['green', 'grey','hsv','blue']:
        raise ValueError('Please input correct method. Valid inputs:''green', 'grey','hsv','blue')
    # if user inputs single image, check for only image formats and pass for further processing
    if is_image== True:
        image = cv2.imread(datapath)
        if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
        #image passes through the mentioned method for colorspace
        #save_image= True will save the image file to the woring directory to view 
        if method == 'green':
            green = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            if save_image==True:
                cv2.imwrite('image_green.jpg', green)
                print('saved')
            colorspace=cv2.imshow('green',green) if show_image==True else green
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        elif method == 'grey':
            bgrgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if save_image==True:
                cv2.imwrite('image_grey.jpg', bgrgray)
                print('saved')      
            colorspace=cv2.imshow('grey',bgrgray) if show_image==True else bgrgray
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        elif method == 'hsv':
            bgrhsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            if save_image==True:
                cv2.imwrite('image_hsv.jpg', bgrhsv)
                print('saved')
            colorspace=cv2.imshow('hsv',bgrhsv) if show_image==True else bgrhsv
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        elif method == 'blue':
            bluei= cv2.cvtColor(image,cv2.COLOR_Lab2BGR)
            if save_image==True:
                cv2.imwrite('image_blue.jpg', bluei)
                print('saved')
            colorspace=cv2.imshow('blue',bluei) if show_image==True else bluei
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
    #if is_image== False, loop continuous to process and check for only image format files for further processing
    elif is_image== False:

        if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): raise ValueError('please provide a valid folder path of images for is_image=False')
        else: pass
        #extract_images function gets activated and images are read and stored into image_path_list
        images_list = extract_images(datapath)
        #creating new list to append all the processed content into rotated_list=[]
        colorspace= []
        #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        image_count = 1
        for i in images_list:
            image = cv2.imread(i)
            #image passes through the mentioned method for colorspace
            if method == 'green':
                green = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
                print('##################### {}'.format(green))
                if save_image==True:
                    cv2.imwrite('image_{}_green.jpg'.format(image_count), green)
                print('saved')        
                colorspaceg=cv2.imshow('green',green) if show_image==True else green
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                colorspace.append(colorspaceg)

            elif method == 'grey':
                bgrgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                if save_image==True:
                    cv2.imwrite('image_{}_grey.jpg'.format(image_count), bgrgray)
                print('saved')
                colorspacegr=cv2.imshow('grey',bgrgray) if show_image==True else bgrgray
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                colorspace.append(colorspacegr)

            elif method == 'hsv':

                bgrhsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                if save_image==True:
                    cv2.imwrite('image_{}_hsv.jpg'.format(image_count), bgrhsv)
                print('saved')
                colorspacehsv=cv2.imshow('hsv',bgrhsv) if show_image==True else bgrhsv
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                colorspace.append(colorspacehsv)
        
            elif method == "blue":              
                bluei= cv2.cvtColor(image,cv2.COLOR_Lab2BGR)
                if save_image==True:
                    cv2.imwrite('image_{}_blue.jpg'.format(image_count), bluei)
                print('saved')
                colorspaceb=cv2.imshow('blue',bluei) if show_image==True else bluei
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                colorspace.append(colorspaceb)
            #image_count gets incrimented everytime a new file gets processed.
            image_count+=1
    #retrning the appended list of processed image data
    return colorspace
#%%
#image_colorspace_opencv('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,'grey',False,False)

#%%  
##segmentation
##segmentation
def image_segmentation_opencv(datapath,is_image,show_image= False,save_image=False):
    # if user inputs single image, check for only image formats and pass for further processing
    #image passes through the mentioned method for segmentation 
    #save_image= True will save the image file to the woring directory to view 
    if is_image== True:
        image = cv2.imread(datapath)
        if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
    #input image gets converted to grayscale image for processing of segmentation
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #cv2.threshold parameters are 
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
        sure_bg = cv2.dilate(opening,kernel,iterations=3)
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers+1
        markers[unknown==255] = 0
        markers = cv2.watershed(image,markers)
        image[markers == -1] = [255,0,0]
        if save_image==True:
            cv2.imwrite('segmentation_image.jpg', image)
        segmentation= cv2.imshow('segmentation',image) if show_image==True else image
    #if is_image== False, loop continuous to process and check for only image format files for further processing.
    elif is_image== False:
        if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): raise ValueError('please provide a valid folder path of images for is_image=False')
        else: pass
        images_list = extract_images(datapath)
        segmentation= []
        image_count = 1
        for i in images_list:
            image = cv2.imread(i)
            #input image gets converted to grayscale image for processing of segmentation
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            #threshold is applied to smooth the image
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            kernel = np.ones((3,3),np.uint8)
            #To use the openig operation, we’ll use the morphologyEx function from the OpenCV Python bindings.
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)   
            #extracting sure background using morphology dilation from the OpenCV Python bindings  
            sure_bg = cv2.dilate(opening,kernel,iterations=3)
            #calculating distance with distaceTransform from the OpenCV Python bindings
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
            #extracting sure foreground
            sure_fg = np.uint8(sure_fg)
            #unknown/ unidentified area from the picture is produced by subtracting fore
            unknown = cv2.subtract(sure_bg,sure_fg)
            ret, markers = cv2.connectedComponents(sure_fg)
            markers = markers+1
            markers[unknown==255] = 0
            markers = cv2.watershed(image,markers)
            image[markers == -1] = [255,0,0]
            segmimg= cv2.imshow('segmentation',image) if show_image==True else image
            if save_image==True:
                cv2.imwrite('segmentation_image_{}.jpg'.format(image_count), image)
            segmentation.append(segmimg) 
            #image_count gets incrimented everytime a new file gets processed.
            image_count+=1
    #retrning the appended list of processed image data
    return segmentation
#%%
#image_segmentation_opencv('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,False,False)
#%%
#RESIZE
#RESIZE
def image_resize_opencv(datapath ,is_image ,method='resize-big',show_image=False, save_image=False, width = None, height = None):
    # if user selects a invalid method we raise an error
    if method not in ['custom', 'resize-small','resize-big','resize-stretch-horizontal','resize-stretch-vertical']:
        raise ValueError('Please input correct method. Valid inputs:''custom', 'resize_small','resize_big','resize-stretch-horizontal','resize-stretch-vertical')
    image = cv2.imread(datapath)
    #print(image)
    # if user inputs single image, check for only image formats and pass for further processing
    if is_image==True:
        if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): pass
        else: raise ValueError('please provide a valid image path for is_image=True')
        #image passes through the mentioned method for resize
        #save_image= True will save the image file to the woring directory to view 
        if method=='custom':
            if width & height == None:
                raise ValueError("please width and height")
            else:
                print('Original Dimensions : ' ,image.shape)
                dim = (width, height)
                resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
                if save_image==True:
                    cv2.imwrite('image_custom_resize.jpg', resized)
                print('Resized Dimensions : ' ,resized.shape)
                #cv2.imshow(image)
                resizec =cv2.imshow('resized',resized) if show_image==True else resized
                cv2.waitKey(0)  
                cv2.destroyAllWindows() 

        elif method == 'resize-small':
            img = image
            print('Original Dimensions : ' ,img.shape)
            scale_percent = 60 # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            if save_image==True:
                cv2.imwrite('image_resize_small.jpg', resized)
            print('Resized Dimensions : ' ,resized.shape)
            resize= cv2.imshow('resized',resized) if show_image==True else resized
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        elif method == 'resize-big':
            img = image
            print('Original Dimensions : ' ,img.shape)
            scale_percent = 220 # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            if save_image==True:
                cv2.imwrite('image_resize_big.jpg', resized)
            print('Resized Dimensions : ' ,resized.shape)
            resize =cv2.imshow('resized',resized) if show_image==True else resized
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        elif method == 'resize-stretch-horizontal':
            img = image
            print('Original Dimensions : ',img.shape)
            width = 440
            height = img.shape[0] # keep original height
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            if save_image==True:
                cv2.imwrite('image_resize_stretch-horizontal.jpg', resized)
            print('Resized Dimensions : ' ,resized.shape)
            resize =cv2.imshow('resized',resized) if show_image==True else resized
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        elif method== 'resize-stretch-vertical':
            print('entered')
            img= image 
            width = img.shape[1] # keep original width
            height = 440
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            print('resized')
            if save_image==True:
                cv2.imwrite('image_resize_stretch-vertical.jpg', resized)
            print('saved')
            resize= cv2.imshow('resized',resized) if show_image==True else resized
            print('resize saved')
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
    #if is_image== False, loop continuous to process and check for only image format files for further processing
    elif is_image== False:
        if (datapath.endswith('.jpeg') or datapath.endswith('.png') or datapath.endswith('.jpg')): raise ValueError('please provide a valid folder path of images for is_image=False')
        else: pass
        #extract_images function gets activated and images are read and stored into image_list
        images_list = extract_images(datapath)
        #creating new list to append all the processed content into rotated_list=[]
        resize = []
        image_count= 1
        #image_count= 1 to intialize to 1 which will get incrimented everytime when a new data enters the list.
        for i in images_list:
            image = cv2.imread(i)
            #image passes through the mentioned method for resize
            if method== 'custom':
                if width & height == None:
                    raise ValueError("please width and height")
                else:
                    print('Original Dimensions : ' ,image.shape)
                    dim = (width, height)
                    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
                    if save_image==True:
                        cv2.imwrite('image_{}_resize_custom.jpg'.format(image_count), resized)
                        print('saved')
                    print('Resized Dimensions : ' ,resized.shape)
                    cv2.imshow('',image)
                    resizec =cv2.imshow('resized',resized) if show_image==True else resized
                    cv2.waitKey(0)
                    cv2.destroyAllWindows() 
                    resize.append(resizec)

            elif method== 'resize-small':
                img = image
                print('Original Dimensions : ' ,img.shape)
                scale_percent = 60 # percent of original size
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                if save_image==True:
                    cv2.imwrite('image_{}_resize_small.jpg'.format(image_count), resized)
                    print('saved')
                    #print('Resized Dimensions : ' ,resized.shape)
                cv2.imshow('',img)
                resizes= cv2.imshow('resized',resized) if show_image==True else resized
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                resize.append(resizes)

            elif method == 'resize-big':
                img = image
                print('Original Dimensions : ' ,img.shape)
                scale_percent = 220
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                if save_image==True:
                    cv2.imwrite('image_{}_resize_big.jpg'.format(image_count), resized)
                print('saved')
                print('Resized Dimensions : ' ,resized.shape)
                cv2.imshow('',img)
                resizeb =cv2.imshow('resized',resized) if show_image==True else resized
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                resize.append(resizeb)

            elif method == 'resize-stretch-horizontal':
                img = image
                print('Original Dimensions : ' ,img.shape)
                width = 440
                height = img.shape[0] 
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                if save_image==True:
                    cv2.imwrite('image_{}_resize-stretch-horizontal.jpg'.format(image_count), resized)
                print('saved')
                print('Resized Dimensions : ' ,resized.shape)
                cv2.imshow('',img)
                resizesh =cv2.imshow('resized',resized) if show_image==True else resized
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                resize.append(resizesh)
            elif method== 'resize-stretch-vertical':
                img = image 
                width = img.shape[1] 
                height = 440
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                if save_image==True:
                    cv2.imwrite('image_{}_resize-stretch-vertical.jpg'.format(image_count), resized)
                print('saved')
                cv2.imshow('', img)
                resizesv= cv2.imshow('resized',resized) if show_image==True else resized
                cv2.waitKey(0)
                cv2.destroyAllWindows() 
                resize.append(resizesv)
            #image_count gets incrimented everytime a new file gets processed.
            image_count+=1
    #retrning the appended list of processed image data   
    return resize


# %%
#image_resize_opencv('C:\\Users\\kavya\\Desktop\\Kavya\\preprocessing_wrappers\\scikit_opencv\\image_data\\elep.jpg',True,'resize-small',show_image=True,save_image=True)

# %%
