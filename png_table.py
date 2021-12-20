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
import argparse


def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the png files are', required=True)
  parser.add_argument('-id', '--ident', type=str, help='Identifier of the images that should be grouped into one table, accepts a comma deliminated list', required=True)
  args = parser.parse_args()
  return(args)
  
  
def mkdir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)


def imageImport(path, identifier):
    Image.MAX_IMAGE_PIXELS = 933120000
    imagelist=[]   
    for i in os.listdir(path):
        matched_ident=[l in i for l in identifier]
        
        if '.png' in i and False not in matched_ident:
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
    png=Image.fromarray(pngRow.astype(np.uint16))
    subfolder=os.path.join(path,''.join(identifier))
    mkdir(subfolder)
    save_path=os.path.join(subfolder, ''.join(identifier) + '_pngMap.png')
    png.save(save_path)
    print('Image saved as {}'.format(save_path))    
            

    return pngRowList, pngRow


def imageCreate(path, rgb, n):
    for i in range(n):
        array = np.zeros([100,100,3], dtype=np.uint8)
        array[:,:100]=rgb
        img=Image.fromarray(array)
        if rgb[0]==0 and rgb[1] == 0 and rgb[2]==0:
            name='black'
        if rgb[0]!=0:
            name='red'
        if rgb[1]!=0:
            name='green'
        if rgb[2]!=0:
            name='blue'
        img.save(os.path.join(path, '{}{}img{}.png'.format(name,n,i)))

if __name__ == '__main__':
    args=parseArguments()   
    path=args.dir
    ident=[str(item) for item in args.ident.split(',')]

    imageImport(path, ident)

    print(args)
    