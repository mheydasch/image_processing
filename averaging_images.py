#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:52:10 2021

@author: max
"""

from PIL import Image
import numpy as np
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

#%%
path='/Volumes/imaging.data/Max/REF52/DLC_1/FRET/FRET_5/FRET_5/Flatfield_s1_/''
#%% flatfield correction
files=os.listdir(path)
ch1='FRET'
ch2='CFP'
ch1reg=re.compile('^.*(?P<Channel1>FRET).*')
ch2reg=re.compile('^.*(?P<Channel2>CFP).*')

ch1List=[]
ch2List=[]

for item in files:
    try:
        if re.search(ch1reg, item).group('Channel1')!=None:
            im=Image.open(os.path.join(path, item))
            imarray=np.array(im)                        
            ch1List.append(imarray)
            ch1listarray=np.array(ch1List) 
# =============================================================================
#            
#         if re.search(ch2reg, item).group('Channel2')!=None:
#             im=Image.open(os.path.join(path, item))
#             imarray=np.array(im)                        
#             ch2List.append(imarray)
#             ch2listarray=np.array(ch2List)
# =============================================================================

    except (AttributeError) as e:
        print(e)
        next
        
ch1averaged=np.median(ch1listarray, axis=0)
ch1tif=Image.fromarray(ch1averaged)
# =============================================================================
# ch2averaged=np.median(ch2listarray, axis=0)
# ch2tif=Image.fromarray(ch2averaged)
# =============================================================================

ch1tif.save(os.path.join(path, ('Averaged_FRET_flatfield.tif')))
#ch1tif.save(os.path.join(path, ('Averaged_CFP_flatfield.tif')))


#%%
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
        
#%%        
ch1_flatfield=np.array(Image.open('/Volumes/imaging.data/Max/REF52/DLC_1/FRET/FRET_8/flatfield/Averaged_FRET_flatfield.tif'))
ch2_flatfield=np.array(Image.open('/Volumes/imaging.data/Max/REF52/DLC_1/FRET/FRET_8/flatfield/Averaged_CFP_flatfield.tif'))
#%%

ch1_flatfield=np.array(Image.open('/Volumes/imaging.data/Max/REF52/DLC_1/FRET/FRET_5/FRET_5/Flatfield_s1_/FRET/Flatfield_s1_w26TIRFFRETacceptor_t3.tif'))
ch2_flatfield=np.array(Image.open('/Volumes/imaging.data/Max/REF52/DLC_1/FRET/FRET_5/FRET_5/Flatfield_s1_/CFP/Flatfield_s1_w16TIRF-CFP_t2.tif'))
path='/Volumes/imaging.data/Max/REF52/DLC_1/FRET/FRET_5/'

ch1='FRET'
ch2='CFP'
output=os.path.join(path, 'flatfield_corrected')
createFolder(output)
#%%

#%%
def bg_calculation(image):
    hist, bins = np.histogram(image, bins=50)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
#    plt.bar(center, hist, align='center', width = width)
#    plt.ylim(0,450000)
#    plt.xlim(0,750)
    bg = np.mean(bins[0:4])
    return bg, #plt.show(
#%%
# Actual background substraction
def background_sub(image, bg):
    global bg_mask
    bg_z_image = image - bg
    bg_mask = np.zeros_like(bg_z_image)
    bg_mask[bg_z_image > 0] = 1
    bg_z_image = bg_mask*bg_z_image
    bg_z_image = bg_z_image.astype(np.float32) 
    return bg_z_image

def bg_correct(image):
    bg_calc = bg_calculation(image)
    corr_im = background_sub(image,bg_calc[0])
    return corr_im

def image_ratioing(f, c, path, FRET):
    FRETimage=f
    CFPimage=c
    FRETratio=np.divide(FRETimage, CFPimage)
    FRETratiotif=Image.fromarray(FRETratio)
    outpath=os.path.join(path, 'ratio')
    createFolder(outpath)
    savestr=os.path.join(outpath,FRET.split('.')[0]+'_ratio'+'.TIF')
    FRETratiotif.save(savestr)
    print('saving: ', savestr)
    
def flatfield_preprocessing(img, flatfield):
    ch1image=np.array(Image.open(os.path.join(path, img)))
    ch1corrected=np.divide(ch1image, flatfield)
    bg_corrected=bg_correct(ch1corrected)
    plt.imshow(bg_corrected, cmap = 'gray')
    return bg_corrected

#%%

def flatfield_correction(path, ch1='FRET', ch2='CFP', timelapse=False):
   files=os.listdir(path)
   if timelapse == False:
       pattern = re.compile('(?P<Imagename>[^w]*).*(?P<Channel>FRET|CFP).*')
   if timelapse == True:       
       pattern = re.compile('(?P<Imagename>[^w]*).*(?P<Channel>FRET|CFP).*(?P<Timepoint>t[0-9]+).*')

   FRET_files=[i for i in files if ch1 in i]
   CFP_files=[i for i in files if ch2 in i] 
   for FRET in FRET_files:
        try:
            if timelapse==False:
                FRETname=re.search(pattern, FRET).group('Imagename')
            if timelapse == True:       
                FRETname=re.search(pattern, FRET).group('Imagename', 'Timepoint')

            FRET_corrected=flatfield_preprocessing(FRET, ch1_flatfield)
            for CFP in CFP_files:
                if timelapse==False:
                    CFPname=re.search(pattern, CFP).group('Imagename')
                    CFPname=re.search(pattern, CFP).group('Imagename', 'Timepoint')

                if CFPname==FRETname:
                    try:
                        CFP_corrected=flatfield_preprocessing(CFP, ch2_flatfield)
                        image_ratioing(FRET_corrected, CFP_corrected, path, FRET)
                        print('processing ', FRET)
                    except OSError as e:
                        print (e)     
            
        except OSError as e:
            print (e)
    
      
#%%

#%%    






    
    

    
    
#%%    
for f, c in zip(FRET_files_corrected, CFP_files_corrected):
    
    FRET=re.search(pattern, f).group('Imagename', 'Timepoint')
    CFP=re.search(pattern, c).group('Imagename', 'Timepoint')
    if FRET==CFP:
        image_ratioing(f, c)

        
    else:
        print(f, c)


#%%
        

# =============================================================================
# im=Image.open(imagepath)
# imarray=np.array(im)                        
# #imList.append(imarray)
# 
# back_subtracted=np.divide(imarray, tif)
# back_subtracted_tif=Image.fromarray(back_subtracted)
# back_subtracted_tif.save('/Users/max/Desktop/test/test.tif')
# =============================================================================
