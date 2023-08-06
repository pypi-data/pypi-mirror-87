#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:10:10 2020

@author: hsjomaa
"""
from ismlldataset.tasks.hpo import Pipeline

class Random(Pipeline):
    def __init__(self, metadataset,evaluation:str):
        super(Random, self).__init__(metadataset=metadataset,evaluation=evaluation)
        
    def run(self,ntrials:int=50,return_results:bool=True):
        self.reset_tracker()
        cs = self.metadataset.get_configuration_space()
        
        while ntrials > 0:
            config = cs.sample_configuration()
            if self.metadataset.is_valid_spec(config):
                self.record(config)
                ntrials-=1
        return self.get_results() if return_results else None