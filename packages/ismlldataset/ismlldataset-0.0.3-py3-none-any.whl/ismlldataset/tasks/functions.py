#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:10:10 2020

@author: hsjomaa
"""
from ismlldataset.tasks.hpo import Pipeline

import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np
from scipy.stats import norm

tfb = tfp.bijectors
tfd = tfp.distributions
tfk = tfp.math.psd_kernels

class Random(Pipeline):
    
    def __init__(self, metadataset):
        
        super(Random, self).__init__(metadataset=metadataset)
        
    def run(self,ntrials:int=50,return_results:bool=True):
        
        self.reset_tracker()
        
        
        suggestions = self.suggest(ntrials=ntrials)
        
        
        [self.record(i) for i in suggestions]
                
        return self.get_results() if return_results else None
    
    def suggest(self,ntrials:int=50):
        
        suggestions = np.arange(self.grid.shape[0])
        
        np.random.shuffle(suggestions)
        
        return suggestions[:ntrials]
    
KERNEL = {
    '32':tfk.MaternThreeHalves,
    '52':tfk.MaternFiveHalves,
    'rbf':tfk.ExponentiatedQuadratic
    }

class GaussianProcess(Pipeline):
    # create Gaussian Process model for linear regression
    def __init__(self,metadataset,kernel:str='32',ninit:int=1):
        # data
        super(GaussianProcess, self).__init__(metadataset=metadataset)
        
        self.kernel = kernel
        
        self.ninit = ninit
        
    def build_gp(self,x):
        
        kernel = tfk.FeatureScaled(KERNEL[self.kernel](self.amplitude_var),scale_diag=self.length_scale_var)
        
        return tfd.GaussianProcess(kernel=kernel,index_points=x,observation_noise_variance=self.observation_noise_variance_var)
        
    def sample(self):
        '''
        Sample from the Joint Gaussian Distribution

        Returns
        -------
        x: tf.Tensor
            Sample of the process.

        '''
        x = self.gp.sample()
        
        return x
    
    def log_prob(self,x):
        '''
        Estimate the log probability of the a sample value

        Parameters
        ----------
        x : tf.Tensor
            DESCRIPTION.

        Returns
        -------
        lp.

        '''
        lp = self.gp.log_prob(x)
        return lp

    def get_trainable_variables(self,ndim):
        constrain_positive = tfb.Shift(np.finfo(np.float64).tiny)(tfb.Exp())
        
        self.amplitude_var = tfp.util.TransformedVariable(
            initial_value=1.,
            bijector=constrain_positive,
            name='amplitude',
            dtype=np.float64)
        
        self.length_scale_var = tfp.util.TransformedVariable(
            initial_value=np.ones(ndim,dtype=np.float64),
            bijector=constrain_positive,
            name='length_scale',
            dtype=np.float64)
        
        self.observation_noise_variance_var = tfp.util.TransformedVariable(
            initial_value=1.,
            bijector=constrain_positive,
            name='observation_noise_variance_var',
            dtype=np.float64)
        
        self.trainable_variables = [v.trainable_variables[0] for v in 
                                [self.amplitude_var,
                                self.length_scale_var,
                                self.observation_noise_variance_var]]
    # Use `tf.function` to trace the loss for more efficient evaluation.
    @tf.function(autograph=False, experimental_compile=False)
    def target_log_prob(self,y):
      return self.gp.log_prob(y)
  
    def suggest(self,gprm,indices,observations):
        
        optimal = max(observations)
        
        mu, stddev     = gprm.mean().numpy(),gprm.stddev().numpy()
        
        mu            = mu.reshape(-1,)
        
        stddev         = stddev.reshape(-1,)
        
        with np.errstate(divide='warn'):
            
            imp = mu - optimal
            
            Z = imp / stddev
            
            ei = imp * norm.cdf(Z) + stddev * norm.pdf(Z)
            
        for _ in range(len(ei)):
            
            if _ in indices:
                
                ei[_] = 0
                
        return np.argmax(ei)        
    
    
    def run(self,ntrials:int=50,return_results:bool=True):
        
        self.reset_tracker()
        
        XC,Y = self.metadataset.get_meta_data(dataset_format="array")
        
        X = self.metadataset.encode_configuration_space(XC)
        
        i = np.random.choice(np.arange(0,X.shape[0]),size=self.ninit,replace=False)
        
        x = X[i]
        
        if x.ndim==1:
            
            x = x[None]
        
        y = Y[i] 
        
        suggestions = i.tolist()
        
        [self.record(i) for i in suggestions]
        
        for t in range(ntrials):
        
            self.get_trainable_variables(ndim=x.shape[1])
            
            self.gp = self.build_gp(x)
            
            optimizer = tf.optimizers.Adam(learning_rate=.01)
    
            losses          = []
            
            bestloss        = np.inf
            
            earlystopping = 0
            
            while earlystopping < 16:
                
                with tf.GradientTape() as tape:
                    
                  loss = -self.target_log_prob(y)
                  
                grads = tape.gradient(loss, self.trainable_variables)
                
                optimizer.apply_gradients(zip(grads, self.trainable_variables))
                
                if abs(bestloss-loss.numpy()) < 1e-3:
                    
                    earlystopping +=1
                    
                else:
                    
                    earlystopping = 0
                    
                    bestloss      = loss.numpy()
                    
                losses.append(loss.numpy())
            
            gprm             = tfd.GaussianProcessRegressionModel(kernel=tfk.FeatureScaled(KERNEL[self.kernel](self.amplitude_var),scale_diag=self.length_scale_var),
                                                                  index_points=X,observation_index_points=x,
                                                                  observations=y,
                                                                  observation_noise_variance=self.observation_noise_variance_var,
                                                                  predictive_noise_variance=0.,)
            
            i = self.suggest(gprm,suggestions,y)
            
            suggestions.append(i)
            
            x = np.vstack([X[_] for _ in suggestions])
            
            y = np.vstack([Y[_] for _ in suggestions]).reshape(-1,)

            self.record(suggestions[-1])
                
        return self.get_results() if return_results else None