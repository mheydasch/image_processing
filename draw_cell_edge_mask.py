#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 13:28:49 2021

@author: max
"""

from scipy import ndimage
from skimage.morphology import binary_erosion
from glob import glob
import numpy as np
import os
import skimage
import pandas as pd
from skimage import io
#%%
project_path = '/Office/Phd/Data/REF52/FRET/FRET_8/testfiles/'
fov = 0
file_name_pattern = "*.tiff"

#
print(file_name_pattern)
filenames = sorted(glob(os.path.join(project_path, file_name_pattern)))
print(filenames[-1])
raw = io.imread(filenames[-1])
#%%
raw = raw[:,400:850,150:700]

print(file_name_pattern)
filenames = sorted(glob.glob(project_path + os.path.join("mask",file_name_pattern)))
print(filenames[-1])
labels = io.imread(filenames[-1])
labels = io.imread(filenames[-1])
labels = labels[400:850,150:700]
labels = skimage.morphology.remove_small_objects(labels, min_size=100**2)
#%%
def spot_mask_from_labels(labels):
    '''takes label mask, shrinks objects and subtracts from original image.'''
    stim_width = 10
    footprint = np.ones((stim_width,stim_width))
    labels_b = labels>0
    labels_b_ero = binary_erosion(labels_b,footprint)
    labels_b_sub = np.logical_xor(labels_b,labels_b_ero)
    labels_b_sub = labels_b_sub.astype('uint8')
    labels_sub = np.multiply(labels_b_sub,labels)
    
    df = pd.DataFrame()
    props = skimage.measure.regionprops(labels)
    for prop in props[:]:
        df_spot = pd.DataFrame({'cell_label': [prop.label],'cell_x': [prop.centroid[0]], 'cell_y':[prop.centroid[1]], 'cell_area': [prop.area],'stim_width':[stim_width]})
        df = df.append(df_spot)

    return labels_b_sub,df