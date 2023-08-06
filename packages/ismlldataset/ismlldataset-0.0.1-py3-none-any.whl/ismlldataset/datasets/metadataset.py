#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:10:28 2020

@author: hsjomaa
"""

import ConfigSpace
import numpy as np
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
class ISMLLMetaDataset(object):
    
    def __init__(self, metadata_file:str,dataset_id:int,evaluation:Union[List[str], str] ='acc',normalize:bool=True):
        self.dataset_id          = dataset_id
        self.metadata_file       = metadata_file
        
        if not os.path.isfile(self.metadata_file):
            raise ValueError(f"Cannot find a meta-data file for dataset {self.dataset_id} at location {''.join(self.metadata_file.split('/')[:-1])} ")
        else:
            self.metadata           = pd.read_csv(self.metadata_file,header=0,delimiter=',',index_col=None)

            self._x  = self.metadata[CONFIG_SPACE]
            if type(evaluation)!=list:
                evaluation = [evaluation]            
            for evalu in evaluation:
                assert evalu in METRICS,(f"The {evaluation} metric of dataset-id {self.dataset_id} is not available!\nTry {','.join(METRICS)}")                
            cols  = []
            for evalu in evaluation:
                cols+=[_ for _ in self.metadata.columns.tolist() if evalu in _]
            self._y = y= self.metadata[cols].round(4)
            if normalize:
                scaler = MinMaxScaler()
                self._y = pd.DataFrame(scaler.fit_transform(np.asarray(y)),columns=y.columns).round(4)
            
        
    def get_meta_data(self,dataset_format: str = 'dataframe',epoch:int=50,fold="valid",
                       hyperparameter: Dict[str,Union[List[str], List[int]]]= None):
        """ Returns metadataset content as dataframes or sparse matrices.

        Parameters
        ----------
        dataset_format : string, optional
            The format of returned dataset.
            If ``array``, the returned dataset will be a NumPy array or a SciPy sparse matrix.
            If ``dataframe``, the returned dataset will be a Pandas DataFrame or SparseDataFrame.

        Returns
        -------
        X : ndarray pr dataframe, shape (n_configurations, n_columns)
            Dataset
        y : ndarray or series, shape (n_samples,)
            Target column(s). Only returned if target is not None.
        """

        x = self._x
        #TODO accomodate different evaluation criteria ? 
        y = self._y[f"{FOLDS[fold]}_acc_{int(epoch/50)-1}"]
        
        if hyperparameter is None:
            return x,np.asarray(y) if dataset_format != 'dataframe' else y
        else:
            cs = self.get_configuration_space()
            xfiltered = []
            for configuration,values in hyperparameter.items():
                if configuration not in CONFIG_SPACE:
                    raise ValueError(f"Configuration {configuration} does not belong to configuration space {','.join(CONFIG_SPACE)}")
                
                if type(values)!=list:
                    values = [values]
                    
                for value in values:
                    if value not in list(cs.get_hyperparameter(configuration).choices):
                        raise ValueError(f"Value {value} is not evaluated for configuration {configuration}\nAvailable configurations include {cs.get_hyperparameter(configuration).choices}")
                    xfiltered.append(x.drop(x[x[configuration]!=value].index,axis=0))
                x = pd.concat(xfiltered,axis=0)
            y = y.loc[x.index]
            return x.reset_index(drop=True),y.reset_index(drop=True) if dataset_format=='dataframe' else np.asarray(y)

    def get_configuration_space(self):
        cs = ConfigSpace.ConfigurationSpace()
        configurationspace = [_ for _ in list(self._x.columns) if '_' not in _]
        for config in configurationspace:
            unique = self._x[config].unique()
            assert(len(unique)>1)
            cs.add_hyperparameter(ConfigSpace.CategoricalHyperparameter(config, unique))
        return cs
    
    def is_valid_spec(self,model_spec):
        configuration         = self.get_metrics_from_spec(self._x,model_spec)        
        return configuration.shape[0] != 0
        
    def get_metrics_from_spec(self,configurations,model_spec):
        if type(model_spec) is dict or type(model_spec)==ConfigSpace.configuration_space.Configuration:
            for cond in model_spec.keys():
                configurations = configurations[configurations[cond]==model_spec[cond]]        
        else:
            for cond in model_spec.columns:
                configurations = configurations[configurations[cond]==model_spec[cond].values[0]]            
        return configurations
    
    def objective_function(self, model_spec,fold:str='valid',evaluation:str='acc',epoch:int=50):
        values = self._y[f"{FOLDS[fold]}_acc_{int(epoch/50)-1}"]
        configuration         = self.get_metrics_from_spec(self._x,model_spec)
        if configuration.shape[0] == 0:
            return (-np.inf, False)
        else:
            if configuration.shape[0] ==1:
                return (values.loc[configuration.index].values.ravel()[0],True)
            else:
                return tuple(values.loc[configuration.index].values.ravel(),)+(True,)
    
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
            return self._x,np.asarray(y)
        elif dataset_format=="dataframe":
            return self._x,y
        else:
            raise(f"Dataset Format {dataset_format} unrecognized, option :['array','dataframe']")


    def get_loss_curve(self,model_spec):
        x,y = self.get_all_loss_curves("dataframe")
        configuration         = self.get_metrics_from_spec(x,model_spec).index.ravel()[0]
        
        y = y.iloc[configuration]
        
        return x.iloc[configuration],np.asarray(y)
    
    def get_all_gradient_curves(self,dataset_format: str = 'array'):
        y = self._get_curves(option="gradient")
        
        if dataset_format=="array":
            return self._x,np.asarray(y)
        elif dataset_format=="dataframe":
            return self._x,y
        else:
            raise(f"Dataset Format {dataset_format} unrecognized, option :['array','dataframe']")


    def get_gradient_curve(self,model_spec):
        x,y = self.get_all_gradient_curves("dataframe")
        configuration         = self.get_metrics_from_spec(x,model_spec).index.ravel()[0]
        
        y = y.iloc[configuration]
        
        return x.iloc[configuration],np.asarray(y)
    

    def response(self,fold:str='valid',epoch:int=50):
        return np.asarray(self._y[f"{FOLDS[fold]}_acc_{int(epoch/50)-1}"])
        
    def optimal(self,fold:str='valid',return_config:bool=True,evaluation:str='acc'):
        y = self.response(fold=fold)
        y_star,y_star_idx  = np.max(y),np.argmax(y)
        return np.asscalar(y_star) if not return_config else (np.asscalar(y_star),self._x.iloc[y_star_idx])        
    
    def unique_evaluations(self,fold:str='valid',evaluation:str='acc'):
        _,y     = self.get_meta_data(evaluation=evaluation,fold=fold)
        return list(np.sort(np.unique(y)))[::-1]

    def rank_evaluation(self,value:float,fold:str='valid',evaluation:str='acc',return_list:bool=False):
        ''' y in descending '''
        y = self.unique_evaluations(fold=fold,evaluation=evaluation)
        if value in y:
            return y.index(value) if not return_list else (y.index(value),y)
        else:
            return np.where(np.asarray(y)-value < 0)[0][0] if not return_list else (np.where(np.asarray(y)-value <0)[0][0] ,y)