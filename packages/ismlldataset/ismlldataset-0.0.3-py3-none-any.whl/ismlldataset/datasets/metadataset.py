#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:10:28 2020

@author: hsjomaa
"""

import ConfigSpace
import numpy as np
import copy
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
from typing import Dict,List,Union

CONFIG_SPACE = ['ACTIVATION',
 'ARCHITECTURE',
 'DROPOUT',
 'LAYERS',
 'NEURONS',
 'NORMALIZATION',
 'OPTIMZERS']

METRICS = ["acc"]

FOLDS = {"train":"trn","valid":"vld","test":"tst"}

SPECIAL_ = {"Layout Md": {"NORMALIZATION":[0],"OPTIMZERS":["adam"],"DROPOUT": [0.0, 0.5], "LAYERS": [3.0, 5.0, 7.0, 1.0], "NEURONS": [4.0, 8.0, 16.0, 32.0], "ACTIVATION": ["relu", "selu"], "ARCHITECTURE": ["ASC", "ENC", "DES", "SQU", "SYM"]},
            "Regularization Md":{"DROPOUT": [0.0, 0.2, 0.5], "LAYERS": [3.0, 5.0, 7.0, 1.0], "NEURONS": [4.0, 8.0, 16.0, 32.0], "ACTIVATION": ["relu", "leaky_relu", "selu"], "NORMALIZATION": [0.0, 1.0],"OPTIMZERS":["adam"],"ARCHITECTURE": ["SQU"]},
            "Optimization Md": {"DROPOUT": [0.0],"LAYERS": [3.0, 5.0, 7.0], "NEURONS": [4.0, 8.0, 16.0], "ACTIVATION": ["relu", "leaky_relu", "selu"], "ARCHITECTURE": ["ASC", "ENC", "DES", "SYM"], "OPTIMZERS": ["adam", "sgd", "rmsprop"], "NORMALIZATION": [0.0],}}

def ptp(X):
    param_nos_to_extract = X.shape[1]
    domain = np.zeros((param_nos_to_extract, 2))
    for i in range(param_nos_to_extract):
        domain[i, 0] = np.min(X[:, i])
        domain[i, 1] = np.max(X[:, i])
    X = (X - domain[:, 0]) / np.ptp(domain, axis=1)
    return X

class ISMLLMetaDataset(object):
    
    def __init__(self, metadata_file:str,dataset_id:int):
        
        self.dataset_id          = dataset_id
        
        self.metadata_file       = metadata_file
        
        self.metafeature_file    = metadata_file.replace("metadataset.dat","metafeatures.dat")
        
        if not os.path.isfile(self.metadata_file):
            
            raise ValueError(f"Cannot find a meta-data file for dataset {self.dataset_id} at location {''.join(self.metadata_file.split('/')[:-1])} ")
            
        else:
            
            self._metafeatures        = np.asarray(pd.read_csv(self.metafeature_file,index_col=None).transpose())
            self.metadata           = pd.read_csv(self.metadata_file,header=0,delimiter=',',index_col=None)
            
            available_responses = []
            
            for fold in FOLDS.keys():
                
                available_responses+= [f"{FOLDS[fold]}_acc_{int(epoch/5)-1}" for epoch in range(5,51,5)]

            self.metadata[available_responses] = np.around(self.metadata[available_responses],4)
            # self.metadata[available_responses] = np.around(0.01*self.metadata[available_responses],4)
            
            self._metadata = copy.deepcopy(self.metadata)

            self.CONFIG_SPACE = copy.deepcopy(CONFIG_SPACE)
    
    @property
    def metafeatures(self):
        return self._metafeatures
    
    def normalize_response(self,):
        
        available_responses = []
        
        for fold in FOLDS.keys():
            
            available_responses+= [f"{FOLDS[fold]}_acc_{int(epoch/5)-1}" for epoch in range(5,51,5)]
            
        scalar = MinMaxScaler()
        
        self.metadata[available_responses] = pd.DataFrame(scalar.fit_transform(np.asarray(self.metadata[available_responses])),columns=available_responses).round(4)
        
    def reset_meta_data(self):
        
        self.metadata = copy.deepcopy(self._metadata)
        
        self.CONFIG_SPACE = copy.deepcopy(CONFIG_SPACE)
    
    def apply_special_transformation(self,special:str):
        
        assert special in SPECIAL_.keys()
        
        self.apply_transformation(hyperparameter=SPECIAL_[special])
        
    def apply_transformation(self,hyperparameter: Dict[str,Union[List[str], List[int]]]):
            
            for k in hyperparameter.keys():
                
                self.metadata = self.metadata[self.metadata[k].isin(hyperparameter[k])]
            
            # get rid of singular configurations
            
            ncs = []
            
            for config in hyperparameter.keys():
                
                unique = self.metadata[config].unique()

                if len(unique)==1:
                    
                    self.metadata = self.metadata.drop([config],axis=1)
                
                else:
                    
                    ncs.append(config)
                
            self.metadata = self.metadata.reset_index(drop=True)
        
            self.CONFIG_SPACE = ncs
        
    def encode_configuration_space(self,X):
        
        X = pd.get_dummies(X).astype(float)
        
        X = ptp(np.asarray(X))
        
        return X
        
    def get_meta_data(self,dataset_format: str = 'dataframe',epoch:int=50,fold="valid",
                      hyperparameter: Dict[str,Union[List[str], List[int]]]=None):
        '''
        

        Parameters
        ----------
        dataset_format : str, optional
            DESCRIPTION. The default is 'dataframe'.
        epoch : int, optional
            DESCRIPTION. Can only choose multiples of 5 up until 50, i.e. (1,5,10,..50). The default is 50.
        fold : TYPE, optional
            DESCRIPTION. The default is "valid". Other options include "test" and "train"
        normalize : bool, optional
            DESCRIPTION. The default is True. Normalize the response 
        hyperparameter : Dict[str,Union[List[str], List[int]]], optional
            DESCRIPTION. The default is None. Restrict the configuration space

        Returns
        -------
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.

        '''
        x = self.metadata[self.CONFIG_SPACE]

        y = pd.DataFrame(self.metadata[f"{FOLDS[fold]}_acc_{int(epoch/5)-1}"])
        
            
        if hyperparameter is None:
            
            return x,np.asarray(y) if dataset_format != 'dataframe' else y
        
        else:
            
            for k in hyperparameter.keys():
                
                x = x[x[k].isin(hyperparameter[k])]
                
            y = y.iloc[x.index]
            
            return x.reset_index(drop=True),y.reset_index(drop=True) if dataset_format=='dataframe' else np.asarray(y)
            
    def get_configuration_space(self,data_format:str="ConfigSpace"):
        
        if data_format=="ConfigSpace":
            cs = ConfigSpace.ConfigurationSpace()
            
            for config in self.CONFIG_SPACE:
                
                unique = self.metadata[config].unique()
                
                assert(len(unique)>1)
                
                cs.add_hyperparameter(ConfigSpace.CategoricalHyperparameter(config, unique))
                
            return cs
        else:
            return self.metadata[self.CONFIG_SPACE]
    
    def is_valid_spec(self,model_spec):
        
        x         = self.get_metrics_from_spec(self.metadata[self.CONFIG_SPACE],model_spec)        
        
        return x.shape[0] != 0
        
    def get_metrics_from_spec(self,configurations,model_spec):
        
        if type(model_spec) is dict or type(model_spec)==ConfigSpace.configuration_space.Configuration:
            
            for cond in model_spec.keys():
                
                configurations = configurations[configurations[cond]==model_spec[cond]]        
        else:
            
            for cond in model_spec.columns:
                
                configurations = configurations[configurations[cond].isin(model_spec[cond])]

        return configurations
    
    def objective_function(self, model_spec,fold:str='valid',epoch:int=50):
        
        y         = self.metadata[f"{FOLDS[fold]}_acc_{int(epoch/5)-1}"]
        
        x         = self.get_metrics_from_spec(self.metadata[self.CONFIG_SPACE],model_spec)
        
        if x.shape[0] == 0:
            
            return (-np.inf, False)
        
        else:
            
            if x.shape[0] ==1:
                
                return (y.loc[x.index].values.ravel()[0],True)
            
            else:
                
                return tuple(y.loc[x.index].values.ravel(),)+(True,)
    
    def _get_curves(self,option:str):
        
        if option=="loss":
            
            keyword = "loss_"
            
        elif option=="gradient":
            
            keyword="gradnorm"
            
        else:
            
            raise(f"Curve information for {option} are not available")
        
        return self.metadata[[_ for _ in self.metadata.columns.tolist() if keyword in _]]
    
    def get_all_loss_curves(self,dataset_format: str = 'array'):
        
        y = self._get_curves(option="loss")
        
        if dataset_format=="array":
            
            return np.asarray(y)
        
        elif dataset_format=="dataframe":
            
            return y
        
        else:
            
            raise(f"Dataset Format {dataset_format} unrecognized, option :['array','dataframe']")


    def get_loss_curve(self,model_spec):
        
        y = self.get_all_loss_curves("dataframe")
        
        configuration         = self.get_metrics_from_spec(self.metadata[self.CONFIG_SPACE],model_spec).index.ravel()[0]
        
        y = y.iloc[configuration]
        
        return np.asarray(y)
    
    def get_all_gradient_curves(self,dataset_format: str = 'array'):
        
        y = self._get_curves(option="gradient")
        
        if dataset_format=="array":
            
            return np.asarray(y)
        
        elif dataset_format=="dataframe":
            
            return y
        
        else:
            
            raise(f"Dataset Format {dataset_format} unrecognized, option :['array','dataframe']")

    def get_gradient_curve(self,model_spec):
        
        y = self.get_all_gradient_curves("dataframe")
        
        configuration         = self.get_metrics_from_spec(self.metadata[self.CONFIG_SPACE],model_spec).index.ravel()[0]
        
        y = y.iloc[configuration]
        
        return np.asarray(y)
    
    
    def response(self,fold:str='valid',epoch:int=50):
        
        return np.asarray(self.metadata[f"{FOLDS[fold]}_acc_{int(epoch/5)-1}"])
        
    def optimal(self,fold:str='valid',return_config:bool=True):
        
        y = self.response(fold=fold)
        
        y_star,y_star_idx  = np.max(y),np.argmax(y)
        
        return np.asscalar(y_star) if not return_config else (np.asscalar(y_star),self.x.iloc[y_star_idx])
    
    def unique_evaluations(self,fold:str='valid',epoch:int=50):
        
        return list(np.sort(np.unique(np.asarray(self.metadata[f"{FOLDS[fold]}_acc_{int(epoch/5)-1}"]))))[::-1]

# TODO Metafeatures!