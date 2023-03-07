import cv2
import numpy as np
import os
from itertools import chain
import pandas as pd


def image_index_cal(directory, path=True):
    '''
    directory is the folder allow user upload images and store csv file
    '''

    #Get list of 
    files = os.listdir(directory)
    
    image_list = []
    
    for file in files:
        if file.endswith(('.png','.bmp','.jpg')):
            image_list.append(file)
            
    
    QI_list = []
    img_quality_list = []
    
    for index in range(len(image_list)):
        
        img_arr = cv2.imread(os.path.join(directory, image_list[index]), 0)
        
        vec_1D = list(chain.from_iterable(img_arr))
        
        low = np.percentile(vec_1D, 1)
        #99% as saturation
        satu = np.percentile(vec_1D, 99)
        #62% as noise
        noise = np.percentile(vec_1D, 30)
        #Mean value of noise and saturation
        middle = np.mean([noise, satu])
        
        #Replace 0 with 1
        if low < 1:
            low = 1
        #Calculate intensity ratio    
        IR = (satu - low) / low * 100
        
        NM_pixels = len(list(x for x in vec_1D if noise <= x <= middle))
        MS_pixels = len(list(y for y in vec_1D if middle < y <= satu))
        
        TSR = MS_pixels / NM_pixels
        
        QI = IR*TSR
        
        if QI >= 500:
            img_quality = 'Good'
        else:
            img_quality = 'Bad'
        
        QI_list.append(QI)
        img_quality_list.append(img_quality)

    #predictions = []
        
    column_dic = {'Image_name':image_list,'Quality_index':QI_list, 'Image_Quality':img_quality_list}

    #predictions.append(column_dic)

    rows = [image_list, QI_list, img_quality_list]
    
    df_name_qi = pd.DataFrame(column_dic, columns =['Image_name', 'Quality_index', 'Image_Quality'], index=range(len(image_list)))

    # Define the output file path
    if path:
        output_path = os.path.join(os.path.dirname(directory), 'predict', 'image_quality.csv')
    else:
        output_path = os.path.join(os.getcwd(), 'predict', 'image_quality.csv')

    out_csv = df_name_qi.to_csv(output_path, index=False)
    
    return out_csv, rows