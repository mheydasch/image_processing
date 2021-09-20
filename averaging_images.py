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
#%%
path='/Volumes/imaging.data/Max/REF52/DLC_1/SiDLC_43/'
#%%
files=os.listdir(path)
ch1=re.compile('^.*_(?P<Channel1>FRET).tif$')
ch2=re.compile('^.*_(?P<Channel2>mTFP).tif$')

imList=[]
for item in files:
    try:
        if re.search(ch1, item).group('Channel1')!=None:
            im=Image.open(os.path.join(path, item))
            imarray=np.array(im)                        
            imList.append(imarray)
            
    except (AttributeError) as e:
        print(e)
        next
#%%        
averaged=np.median(np.array(newlist), axis=0)
tif=Image.fromarray(averaged)
im.save(os.path.join(path, ('Averaged_'+ item)))



# =============================================================================
# im=Image.open(imagepath)
# imarray=np.array(im)                        
# #imList.append(imarray)
# 
# back_subtracted=np.divide(imarray, tif)
# back_subtracted_tif=Image.fromarray(back_subtracted)
# back_subtracted_tif.save('/Users/max/Desktop/test/test.tif')
# =============================================================================
