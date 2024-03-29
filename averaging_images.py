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
files=os.listdir(path)
ch1='FRET'
ch2='CFP'
output=os.path.join(path, 'flatfield_corrected')
createFolder(output)
#%%
FRET_files=[i for i in files if ch1 in i]
CFP_files=[i for i in files if ch2 in i]
#%%

#%%
for item in FRET_files:
    ch1image=np.array(Image.open(os.path.join(path, item)))
    ch1corrected=np.divide(ch1image, ch1_flatfield)
    ch1corrected=ch1corrected*10000
    ch1tif=Image.fromarray(ch1corrected)
    outpath=os.path.join(output, item)
    FRET_files_corrected.append(item)
    ch1tif.save(outpath)
    
    
    print('saving ', item)
FRET_files_corrected=sorted(FRET_files_corrected)
#%%
for item in CFP_files:
    ch2image=np.array(Image.open(os.path.join(path, item)))
    ch2corrected=np.divide(ch2image, ch2_flatfield)
    ch2corrected=ch2corrected*10000
    ch2tif=Image.fromarray(ch2corrected)
    outpath=os.path.join(output, item)
    CFP_files_corrected.append(item)
    ch2tif.save(outpath)
    print('saving ', item)
CFP_files_corrected=sorted(CFP_files_corrected)
#%%    
pattern = re.compile('(?P<Imagename>[^w]*).*(?P<Channel>FRET|CFP).*')
pattern = re.compile('(?P<Imagename>[^w]*).*(?P<Channel>FRET|CFP).*(?P<Timepoint>t[0-9]+).*')

output=os.path.join(path, 'flatfield_corrected')
ratiofolder=os.path.join(path, 'ratio2')
createFolder(ratiofolder)
pairs=pd.DataFrame()



def image_ratioing(f, c):
    FRETimage=np.array(Image.open(os.path.join(output, f)))
    CFPimage=np.array(Image.open(os.path.join(output, c)))
    FRETratio=np.divide(FRETimage, CFPimage)
    FRETratiotif=Image.fromarray(FRETratio)
    savestr=os.path.join(ratiofolder,f.split('.')[0]+'_ratio'+'.TIF')
    FRETratiotif.save(savestr)
    print('saving: ', savestr)

    
    

    
    
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
