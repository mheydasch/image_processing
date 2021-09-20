#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:52:07 2021

@author: max
"""

import numpy as np
import pandas as pd
import imageio
import os
import math
from PIL import Image
def mkdir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
Image.MAX_IMAGE_PIXELS = 933120000

def imageImport(path, identifier):
    imagelist=[]
    for i in os.listdir(path):
        
        if '.png' in i and identifier in i:
            print(i)
            im=imageio.imread(os.path.join(path,i))
            imagelist.append(im)
    imageShape=im.shape
    tableShape=math.ceil(math.sqrt(len(imagelist)))
    print(tableShape)
    print(im.shape)
    imageShape=im.shape
    pngRow=np.arange(imageShape[0]*imageShape[1])
    pngRow=pngRow.reshape((imageShape[0], imageShape[1]))
    
    
    pngRowList=[]
    columnCount=1
    rowCount=1
    while columnCount <=tableShape:
     
        for i in imagelist:
            print(i)
            print('tableShape', tableShape)
            print('columnCount:', columnCount)
            print('rowCount:', rowCount)
            pngRow=np.concatenate((pngRow, i), axis=1)
            print(pngRow.shape)
            columnCount+=1
            if columnCount > tableShape:
                rowCount+=1
                if rowCount > tableShape:
                   break
                pngRowList.append(pngRow)
                
                columnCount=1
                pngRow=np.arange(imageShape[0]*imageShape[1])
                pngRow=pngRow.reshape((imageShape[0], imageShape[1]))

    for p in pngRowList:
        pngRow=np.concatenate((pngRow, p))
        print('png shape:',pngRow.shape) 
    to_del=list(range(0, imageShape[0]))
    pngRow=np.delete(pngRow, to_del, axis=1)
    png=Image.fromarray(pngRow.astype(np.uint8))
    subfolder=os.path.join(path,identifier)
    mkdir(subfolder)
    save_path=os.path.join(subfolder, identifier + '_pngMap.png')
    png.save(save_path)
    print('Image saved as {}'.format(save_path))    
            

    return pngRowList, pngRow


def imageCreate(path):
    for i in range(40):
        array = np.zeros([100,100,3], dtype=np.uint8)
        array[:,:100]=[0,0,0]
        img=Image.fromarray(array)
        img.save(os.path.join(path, 'black2img{}.png'.format(i)))
    
    