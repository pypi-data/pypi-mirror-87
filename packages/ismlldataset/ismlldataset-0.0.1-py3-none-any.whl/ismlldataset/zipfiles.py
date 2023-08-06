#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 12:27:56 2020

@author: hsjomaa
"""

import os
import zipfile
import pandas as pd
import shutil
ms = pd.read_csv('/home/hsjomaa/exhaustive-meta-dataset/results/49.csv')
path = '/home/hsjomaa/cross_task_surrogate_learning/data/repo/origin/'
temp = '/home/hsjomaa/temp/'
os.makedirs(temp)
maps = {}
for dataset_id,folder in enumerate(os.listdir(path)):
    maps.update({dataset_id:folder})
    shutil.copy(f'{path}{folder}/{folder}_py.dat',f'{temp}features.dat')
    shutil.copy(f'{path}{folder}/labels_py.dat',f'{temp}labels.dat')
    columns = list(ms.columns)[:7] + [_ for _ in list(ms.columns) if folder in _]
    ms[columns].to_csv(f'{temp}metadataset.dat',index=False)
    file_paths = [_ for _ in os.listdir(temp)]
    # writing files to a zipfile 
    with zipfile.ZipFile(f'/home/hsjomaa/zipped/{dataset_id}.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths: 
            zip.write(os.path.join(temp,file),file)
    [os.remove(os.path.join(temp,_)) for _ in os.listdir(temp)]