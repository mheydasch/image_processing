#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 11:21:19 2021

@author: max
"""

from PIL import Image
import numpy as np
import os
import re
import argparse

#%% Image_substraction
imagepath='/Volumes/imaging.data/Max/REF52/DLC_1/SiDLC_43/'
def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='subtract a Flatfield image from all images in the folder')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the images are', required=True)
  parser.add_argument('-ff', '--flatf', type=str, help='the flatfield image', required =True)
  args = parser.parse_args()
  return(args)
  
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def subtractFlatfield(path, flatfield):
    ch1=re.compile('^.*_(?P<Channel1>FRET).tif$')
    ch2=re.compile('^.*_(?P<Channel2>mTFP).tif$')
    files=os.listdir(path)
    ff=Image.open(flatfield)
    flatf=np.array(ff)
    for item in files:
        try:
            if re.search(ch1, item).group('Channel1')!=None:
                im=Image.open(os.path.join(path, item))
                imarray=np.array(im)                        
                back_subtracted=np.divide(imarray, flatf)
                back_subtracted_tif=Image.fromarray(back_subtracted)
                saveFolder=os.path.join(path, 'flatfield_corrected')
                createFolder(saveFolder)
                back_subtracted_tif.save(os.path.join(saveFolder, ('Flatcorr_'+ item)))
                print(item, 'processed')
        except (AttributeError) as e:
            print(e)
            next


if __name__ == '__main__':
    args=parseArguments()
    path=args.dir
    flatfield=args.flatf
    subtractFlatfield(path, flatfield)
    print(args)