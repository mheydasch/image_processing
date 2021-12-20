#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 23:07:24 2021

@author: max
"""
import shutil
import os
import re

import argparse

def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the knockdown folders are', required=True)
  parser.add_argument('-l', '--length', type=str, help='how long is the timelapse supposed to be', required=True)
  #parser.add_argument('-p', '--prefix', type=str, help='prefix of the movie', required=True)

  args = parser.parse_args()
  return(args)
def create_timelapse(path, length, prefix=''):
    length=list(range(length))
    length=[str(i) for i in length]
    length=[i.zfill(5) for i in length]
    files=os.listdir(path)
    print(files)
    pattern = re.compile('(?P<Channel>mask).*(?P<FOV>[0-9]{2})_(?P<Timepoint>[0-9]{5}).tiff')
    for item in files:
        print(item)
        Timepoint=re.search(pattern, item).group('Timepoint')
        #[shutil.copyfile(os.path.join(path, item), os.path.join(path, item.replace(Timepoint, t))) for t in length]
        for t in length:
            print(t)
            temp=os.path.join(path, prefix, item.replace(Timepoint, t))
            print(item)
            if Timepoint!=t:
                shutil.copyfile(os.path.join(path,item), temp)
            
        print('created timelapse of ', os.path.join(path, item))
        
if __name__ == '__main__':
    args=parseArguments()
    path=args.dir
    length=args.length
    #prefix=args.prefix
    create_timelapse(path, length)