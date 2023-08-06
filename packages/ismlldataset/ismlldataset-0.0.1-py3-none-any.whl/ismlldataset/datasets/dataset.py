import logging
import os
from typing import List, Optional, Union
from sklearn.model_selection import KFold,train_test_split
import numpy as np
import pandas as pd
from ..utils import _create_cache_directory_for_id
DATASETS_CACHE_DIR_NAME = 'datasets'

logger = logging.getLogger(__name__)


class ISMLLDataset(object):

    def __init__(self,dataset_id,data_file,target_file,folds,validation_folds):

        self.dataset_id = int(dataset_id) if dataset_id is not None else None
        self.data_file = data_file
        self.target_file = target_file
        self.folds = folds
        self.validation_folds = validation_folds
#TODO EXTRACT META_FEATURES
#        if features is not None:
#            self.features = {}
#            # todo add nominal values (currently not in database)
#            for idx, xmlfeature in enumerate(features['oml:feature']):
#                nr_missing = xmlfeature.get('oml:number_of_missing_values', 0)
#                feature = OpenMLDataFeature(int(xmlfeature['oml:index']),
#                                            xmlfeature['oml:name'],
#                                            xmlfeature['oml:data_type'],
#                                            xmlfeature.get('oml:nominal_value'),
#                                            int(nr_missing))
#                if idx != feature.index:
#                    raise ValueError('Data features not provided '
#                                     'in right order')
#                self.features[feature.index] = feature

    @staticmethod
    def _convert_array_format(data, array_format):
        """Convert a dataset to a given array format.

        By default, the data are stored as a sparse matrix or a pandas
        dataframe. One might be interested to get a pandas SparseDataFrame or a
        NumPy array instead, respectively.
        """
        if array_format == "array" and hasattr(data,'iloc'):
            return np.asarray(data)
        else:
            return data
    
    def get_folds(self,split:int,n_splits:int = 5,random_state:int =0,return_valid:bool=True):
        """ Returns train and test split.

        Parameters
        ----------
        split : int
            the split of the dataset
        n_splits : int,
            total number of splits
        random_state: int,optional
            random seed of model_selection 
        return_valid: bool
            return validation set
            
        Returns
        -------
        X : ndarray, dataframe, or sparse matrix, shape (n_samples, n_columns)
            Dataset
        y : ndarray or series, shape (n_samples,)
            Target column(s). Only returned if target is not None.
        """        
        x,y = self.get_data(dataset_format='array')
        cache_directory  = _create_cache_directory_for_id(DATASETS_CACHE_DIR_NAME, self.dataset_id)
        if self.folds is None:
            split_generator  = KFold(n_splits=n_splits,random_state=random_state,shuffle=True)
            split_generator.get_n_splits(x)
            splits = [_ for _ in split_generator.split(x)]
            q=[]
            for index_tuple in splits:
                train,test = index_tuple
                tmp = np.zeros(shape=x.shape[0],dtype=int)
                tmp[test]=1
                q.append(tmp)
            q = pd.DataFrame(np.vstack(q).transpose())
            self.folds = os.path.join(cache_directory,'folds.dat')
            q.to_csv(self.folds,header=None,index=None)
        
        if self.validation_folds is None and return_valid:
            split_generator  = KFold(n_splits=n_splits,random_state=random_state,shuffle=True)
            split_generator.get_n_splits(x)            
            splits = [_ for _ in split_generator.split(x)]
            p = []
            train_val_indices = [train_test_split(_,test_size=0.2) for _ in [_[0] for _ in splits]]
            for index_tuple in train_val_indices:
                train,val = index_tuple
                tmp = np.zeros(shape=x.shape[0],dtype=int)
                tmp[val]=1
                p.append(tmp)                
            p = pd.DataFrame(np.vstack(p).transpose())
            self.validation_folds = os.path.join(cache_directory,'validation_folds.dat')
            p.to_csv(self.validation_folds,header=None,index=None)
            
        fold            = np.asarray(pd.read_csv(self.folds,header=None)[split])
        xtest  = x[fold==1]
        ytest  = y[fold==1]
        if return_valid:
            validation_fold = np.asarray(pd.read_csv(self.validation_folds,header=None)[split])
            xtrain = x[(validation_fold==0) & (fold==0)]
            xval   = x[validation_fold==1]
            x = (xtrain,xval,xtest)
            
            ytrain = y[(validation_fold==0) & (fold==0)]
            yval   = y[validation_fold==1]
            y = (ytrain,yval,ytest)
            
            return x,y
        else:
            xtrain = x[fold==0]
            ytrain = y[fold==0]
            
            x = (xtrain,xtest)
            y = (ytrain,ytest)
            return x,y
    
    def get_data(self, target: Optional[Union[List[str], str]] = None,
                       dataset_format: str = 'dataframe'):
        """ Returns dataset content as dataframes or sparse matrices.

        Parameters
        ----------
        dataset_format : string, optional
            The format of returned dataset.
            If ``array``, the returned dataset will be a NumPy array or a SciPy sparse matrix.
            If ``dataframe``, the returned dataset will be a Pandas DataFrame or SparseDataFrame.

        Returns
        -------
        X : ndarray, dataframe, or sparse matrix, shape (n_samples, n_columns)
            Dataset
        y : ndarray or series, shape (n_samples,)
            Target column(s). Only returned if target is not None.
        """

        if not os.path.isfile(self.data_file) or not os.path.isfile(self.target_file):
            raise ValueError(f"Cannot find a data or target file for dataset {self.dataset_id} at location {''.join(self.data_file.split('/')[:-1])} ")
        else:
            data = pd.read_csv(self.data_file,header=None,delimiter=',',index_col=None)

        if target is None:
            y    = self._convert_array_format(pd.read_csv(self.target_file,header=None,delimiter=',',index_col=None),dataset_format)
            x    = self._convert_array_format(data, dataset_format,)
            assert(x.shape[0]==y.shape[0])
            return x,y
        else:
            if isinstance(target, str):
                if ',' in target:
                    target = [int(_) for _ in target.split(',')]
                else:
                    target = [int(target)]
            
            y       = pd.read_csv(self.target_file,header=None,delimiter=',',index_col=None)
            targets = []
            for tar in target:
                targets.append(y[y[y.columns[0]]==tar])
            y = pd.concat(targets,axis=0)
            x = data.iloc[y.index]
            x    = self._convert_array_format(x, dataset_format,)
            y    = self._convert_array_format(y, dataset_format,)
            return x,y
