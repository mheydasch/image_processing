#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 21:00:17 2022

@author: max
"""

import shutil
import os
import re
import skimage
import argparse
from PIL import Image, ImageSequence
import numpy as np
from skimage import io
def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the knockdown folders are', required=True)
  parser.add_argument('-l', '--length', type=int, help='how long is the timelapse supposed to be', required=True)
  parser.add_argument('-p', '--prefix', type=str, help='prefix of the movie', required=False)
  parser.add_argument('-c', '--channel', type=int, help='how long is the timelapse supposed to be', required=False)


  args = parser.parse_args()
  return(args)
  
  
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
        
def split_RGB_timelapse(path, length, prefix='', channel=2):
    length=list(range(length))
    length=[str(i) for i in length]
    length=[i.zfill(5) for i in length]
    files=os.listdir(path)
    print(files)
    pattern = re.compile('(?P<Channel>).*(?P<FOV>[0-9]{2})_(?P<Timepoint>[0-9]{5}).tiff')
    for item in files:
        print(item)
        try:
            Timepoint=re.search(pattern, item).group('Timepoint')
            img=io.imread(os.path.join(path, item))
            stack=np.squeeze(img)
        except: 
            continue

        #[shutil.copyfile(os.path.join(path, item), os.path.join(path, item.replace(Timepoint, t))) for t in length]
        for t in length:
            print(t)
            createFolder(os.path.join(path,'split_timelapse'))
            temp=os.path.join(path, 'split_timelapse', prefix, item.replace(Timepoint, t))
            print(item)
            skimage.io.imsave(temp, stack[:,:,2])
    print('created timelapse of ', os.path.join(path, item))
            
       
#%%        
if __name__ == '__main__':
    args=parseArguments()
    path=args.dir
    length=args.length
    prefix=args.prefix
    channel=args.channel
    split_RGB_timelapse(path, length, prefix, channel)