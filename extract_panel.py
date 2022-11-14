# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 11:30:29 2022

@author: Gabriel
"""

import cv2
import pytesseract
import matplotlib.pyplot as plt
import numpy as np

px = 1/plt.rcParams['figure.dpi'] 

# Load the image
path_img = "C:/Users/Gabriel/Documents/_Documents/Etudes/\
3A/9.6 Deep Learning/Projet DL/raw_data/Jesse_James_09__JVJ_Soothsayer_DMiles/\
30.jpg"
# path_img = "C:/Users/Gabriel/Documents/_Documents/Etudes/3A/9.6 Deep Learning/Projet DL/case_test1.png"
image = cv2.imread(path_img)

path = "C:/Users/Gabriel/Documents/_Documents/Etudes/\
3A/9.6 Deep Learning/Projet DL/raw_data/Jesse_James_09__JVJ_Soothsayer_DMiles/"

#%%

def extract_image_contour(image_, contour, fill_color=(255,255,255)):
    x,y,w,h = cv2.boundingRect(contour)
    mask = np.ones((image_.shape[0], image_.shape[1],3), dtype=np.bool8)
    mask[ y:y+h,x:x+w,:] = False
    extracted_image = image_.copy()
    np.putmask(extracted_image, mask, fill_color)
    # extracted_image = image_.copy()[x:x+w,y:y+h,:]
    # print(extracted_image.shape)
    return extracted_image

def extract_strips(original_image):
    
    image = original_image.copy()
    image = cv2.GaussianBlur(image,(3,3),cv2.BORDER_DEFAULT)

    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(gray, 100, 200)
    
    
    
    # downsampled_edges = cv2.pyrDown(cv2.pyrDown(edges))
    downsampled_edges = cv2.pyrDown(edges)
    # image_ds = cv2.pyrDown(cv2.pyrDown(image))
    image_ds = cv2.pyrDown(image)
    
    
    contours_ds,hierarchy_ds = cv2.findContours(downsampled_edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # image_ds_cont = cv2.drawContours(image_ds, contours_ds, -1, (0, 255, 0), 2)
    # hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
    
    area_list = []

    image_ds_cont = image_ds.copy()
    image_cont = original_image.copy()
    list_panels = []
    for c in contours_ds:
        currentContour = c
        x,y,w,h = cv2.boundingRect(currentContour)
        
        area = cv2.contourArea(currentContour, True)

        area_list.append(area)
        if abs(area) > 8000:
            image_ds_cont = cv2.drawContours(image_ds_cont, currentContour, -1, (0, 255, 0), 2)
            image_cont = cv2.drawContours(image_cont, currentContour*2, -1, (0, 255, 0), 2)
            extracted_image=extract_image_contour(image,currentContour*2)
            list_panels.append(extracted_image)
        #     # plt.subplots(figsize=(2000*px, 1500*px)); plt.axis("off")
        #     # plt.imshow(cv2.cvtColor(extracted_image, cv2.COLOR_BGR2RGB))
        #     # plt.show()
            

    # plt.subplots(figsize=(2498*px, 1704*px)); plt.axis("off")
    # plt.imshow(cv2.cvtColor(image_ds_cont, cv2.COLOR_BGR2RGB))
    # plt.show()
    return image_cont, list_panels


# extract_strips(image)
#%%

for i in range(1,36):
    if i not in [1,2,9,34,35,18,19,26,27]:
        path_img_ = path + "{:02d}.jpg".format(i)
        image = cv2.imread(path_img_)
        strips, panels = extract_strips(image)
        cv2.imwrite("test_extract/strips/{:02d}.png".format(i),strips)
        for j in range(len(panels)):
            cv2.imwrite("test_extract/panels/{:02d}_{:02d}.png".format(i,j),panels[j])