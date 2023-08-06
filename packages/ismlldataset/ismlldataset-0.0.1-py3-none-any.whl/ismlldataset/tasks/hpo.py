#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:56:37 2020

@author: hsjomaa
"""

import numpy as np
import pandas as pd

def regret(output,response,fold="valid"):
    incumbent   = output[0]
    best_output = []
    for _ in output:
        incumbent = _ if _ > incumbent else incumbent
        best_output.append(incumbent)
    opt       = max(response)
    orde      = list(np.sort(np.unique(response))[::-1])
    tmp       = pd.DataFrame(best_output,columns=[f'regret_{fold}'])
    
    tmp[f'rank_{fold}']        = tmp[f'regret_{fold}'].map(lambda x : orde.index(x))
    tmp[f'regret_{fold}'] = opt - tmp[f'regret_{fold}']
    return tmp

class Pipeline(object):
    def __init__(self, metadataset,evaluation:str):
        
        
        self.metadataset = metadataset
        self.evaluation = evaluation
        self.y_star_valid = self.metadataset.optimal(fold='valid',evaluation=evaluation,return_config=False)
        self.y_star_test  = self.metadataset.optimal(fold='test',evaluation=evaluation,return_config=False)
        
        self.response_vld = self.metadataset.response(fold="valid")
        self.response_tst = self.metadataset.response(fold="test")
        self.X = []
        self.y_valid = []
        self.y_test = []
        
    def reset_tracker(self):
        self.X       = []
        self.y_valid = []
        self.y_test  = []

    def record(self,config):
       self.X.append(config)
       
       valid_score,is_valid = self.metadataset.objective_function(fold='valid',evaluation=self.evaluation,model_spec=config)
       assert(is_valid)
        
       self.y_valid.append(valid_score)
        
       test_score,is_valid = self.metadataset.objective_function(fold='test',evaluation=self.evaluation,model_spec=config)
       
       assert(is_valid)
        
       self.y_test.append(test_score)
        
    def get_results(self, ignore_invalid_configs=False,data_format='dataframe'):

        res = pd.DataFrame(data=None)
        
        vld = regret(output=self.y_valid,response=np.asarray(self.response_vld),fold="valid")
        
        res = pd.concat([res,vld],axis=1)

        tst = regret(output=self.y_test,response=np.asarray(self.response_tst),fold="test")
        
        res = pd.concat([res,tst],axis=1)
        

        return np.asarray(res) if data_format !='dataframe' else res
    
    def run(self,ntrials:int=50,return_results:bool=True):
        raise("Not implemented")