#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:57:48 2020

@author: hsjomaa
"""
import os
import zipfile
import pandas as pd
import shutil

rootdir     = os.path.dirname(os.path.realpath(__file__))


path = '/home/hsjomaa/cross_task_surrogate_learning/data/repo/origin/'
temp = '/home/hsjomaa/temp/'
os.makedirs(temp,exist_ok=True)
maps = {}
ss = [_ for _ in os.listdir(path) if _!="trains"]
for dataset_id,folder in enumerate(ss):
    maps.update({dataset_id:folder})
    shutil.copy(os.path.join(path,folder,f"{folder}_py.dat"),os.path.join(temp,"features.dat"))
    shutil.copy(os.path.join(path,folder,"labels_py.dat"),os.path.join(temp,"labels.dat"))
    read_metadataset = pd.read_csv(os.path.join(rootdir,"raw",f"{folder}.csv"),header=0,index_col=0)
    # columns = list(ms.columns)[:7] + [_ for _ in list(ms.columns) if folder in _]
    read_metadataset.to_csv(os.path.join(temp,"metadataset.dat"),index=False)
    file_paths = [_ for _ in os.listdir(temp)]
    assert(len(file_paths)==3)
    # writing files to a zipfile 
    with zipfile.ZipFile(f'/home/hsjomaa/zipped/{dataset_id}.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths: 
            zip.write(os.path.join(temp,file),file)
    [os.remove(os.path.join(temp,_)) for _ in os.listdir(temp)]