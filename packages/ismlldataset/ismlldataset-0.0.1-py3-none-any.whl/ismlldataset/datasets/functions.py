#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:33:10 2020

@author: hsjomaa
"""
from typing import Union,List
from ..utils import _remove_cache_dir_for_id,_create_cache_directory_for_id,_create_cache_directory,_download_zip_file
from ..config import _get_dataset_url
from .dataset import ISMLLDataset
from .metadataset import ISMLLMetaDataset
import os

DATASETS_CACHE_DIR_NAME = 'datasets'

def get_datasets(
        dataset_ids: List[Union[str, int]],
        download_data: bool = True,
) -> List[ISMLLDataset]:
    """Download datasets.

    This function iterates :meth:`openml.datasets.get_dataset`.

    Parameters
    ----------
    dataset_ids : iterable
        Integers or strings representing dataset ids.
    download_data : bool, optional
        If True, also download the data file. Beware that some datasets are large and it might
        make the operation noticeably slower. Metadata is also still retrieved.
        If False, create the ISMLLDataset and only populate it with the metadata.
        The data may later be retrieved through the `ISMLLDataset.get_data` method.

    Returns
    -------
    datasets : list of datasets
        A list of dataset objects.
    """
    datasets = []
    for dataset_id in dataset_ids:
        datasets.append(get_dataset(dataset_id, download_data))
    return datasets

def get_dataset(dataset_id: Union[int, str], download_data: bool = True) -> ISMLLDataset:
    """ Download the OpenML dataset representation, optionally also download actual data file.

    This function is thread/multiprocessing safe.
    This function uses caching. A check will be performed to determine if the information has
    previously been downloaded, and if so be loaded from disk instead of retrieved from the server.

    Parameters
    ----------
    dataset_id : int or str
        Dataset ID of the dataset to download
    download_data : bool, optional (default=True)
        If True, also download the data file. Beware that some datasets are large and it might
        make the operation noticeably slower. Metadata is also still retrieved.
        If False, create the ISMLLDataset and only populate it with the metadata.
        The data may later be retrieved through the `ISMLLDataset.get_data` method.

    Returns
    -------
    dataset : :class:`openml.ISMLLDataset`
        The downloaded dataset."""
    try:
        dataset_id = int(dataset_id)
    except (ValueError, TypeError):
        raise ValueError("Dataset ID is neither an Integer nor can be "
                         "cast to an Integer.")

    did_cache_dir = _create_cache_directory_for_id(DATASETS_CACHE_DIR_NAME, dataset_id,)
    if not os.path.isfile(os.path.join(did_cache_dir,"features.dat")) and not os.path.isfile(os.path.join(did_cache_dir,"labels.dat")):
        source = _get_dataset_url(dataset_id=dataset_id)
        _download_zip_file(source=source,output_path=did_cache_dir)
    try:
        remove_dataset_cache = True

        features = _get_dataset_description(description='features', dataset_id=dataset_id,cache_directory=did_cache_dir)
        labels   = _get_dataset_description(description='labels', dataset_id=dataset_id,cache_directory=did_cache_dir)
        folds    = _get_dataset_description(description='folds', dataset_id=dataset_id,cache_directory=did_cache_dir)
        validation_folds = _get_dataset_description(description='validation_folds', dataset_id=dataset_id,cache_directory=did_cache_dir)
        remove_dataset_cache = False
    except Exception as e:
        # if there was an exception,
        # check if the user had access to the dataset
#        if e.code == 112:
#            raise OpenMLPrivateDatasetError(e.message) from None
#        else:
#            raise e
        print(e,did_cache_dir)
    finally:
        if remove_dataset_cache:
            _remove_cache_dir_for_id(DATASETS_CACHE_DIR_NAME,did_cache_dir)

    dataset = _create_dataset_from_description(dataset_id,features, labels, folds, validation_folds)
    return dataset


def get_metadataset(dataset_id: Union[int, str], download_data: bool = True) -> ISMLLMetaDataset:
    """ Download the OpenML dataset representation, optionally also download actual data file.

    This function is thread/multiprocessing safe.
    This function uses caching. A check will be performed to determine if the information has
    previously been downloaded, and if so be loaded from disk instead of retrieved from the server.

    Parameters
    ----------
    dataset_id : int or str
        Dataset ID of the dataset to download
    download_data : bool, optional (default=True)
        If True, also download the data file. Beware that some datasets are large and it might
        make the operation noticeably slower. Metadata is also still retrieved.
        If False, create the ISMLLDataset and only populate it with the metadata.
        The data may later be retrieved through the `ISMLLDataset.get_data` method.

    Returns
    -------
    dataset : :class:`openml.ISMLLDataset`
        The downloaded dataset."""
    try:
        dataset_id = int(dataset_id)
    except (ValueError, TypeError):
        raise ValueError("Dataset ID is neither an Integer nor can be "
                         "cast to an Integer.")

    did_cache_dir = _create_cache_directory_for_id(DATASETS_CACHE_DIR_NAME, dataset_id,)
    if not os.path.isfile(os.path.join(did_cache_dir,"metadataset.dat")):
        source = _get_dataset_url(dataset_id=dataset_id)
        _download_zip_file(source=source,output_path=did_cache_dir)
        
    try:
        remove_dataset_cache = True

        metadataset = _get_dataset_description(description='metadataset', dataset_id=dataset_id,cache_directory=did_cache_dir)
        remove_dataset_cache = False
    except Exception as e:
        # if there was an exception,
        # check if the user had access to the dataset
#        if e.code == 112:
#            raise OpenMLPrivateDatasetError(e.message) from None
#        else:
#            raise e
        print(e,did_cache_dir)
    finally:
        if remove_dataset_cache:
            _remove_cache_dir_for_id(DATASETS_CACHE_DIR_NAME,did_cache_dir)

    dataset = _create_metadataset_from_description(dataset_id,metadataset)
    return dataset

def _get_dataset_description(description:str,dataset_id: int,cache_directory=None) -> str:
    """API call to get dataset description (cached)

    Description includes labels/folds/features

    Parameters
    ----------
    description : str
        Dataset aspect
    
    did_cache_dir : str
        Cache subdirectory for this dataset

    dataset_id : int
        Dataset ID

    Returns
    -------
    output_file_path : string
        Location of dataset description file.
    """
    if cache_directory is None:
        cache_directory = _create_cache_directory_for_id(DATASETS_CACHE_DIR_NAME, dataset_id)
    output_file_path = os.path.join(cache_directory, f"{description}.dat")

    if not os.path.isfile(output_file_path) and description not in ['validation_folds','folds']:
            raise(f'{description}.dat not available at {cache_directory}')
    elif description in ['validation_folds','folds']:
        return None
    else:
#            shutil.copy(os.path.join(get_local_directory(),str(dataset_id),f"{description}.dat"),output_file_path)
        return output_file_path


def _create_dataset_from_description(
        dataset_id:int,
        features: str,
        labels: str,
        folds: str = None,
        validation_folds:str=None
) -> ISMLLDataset:
    """Create a dataset object from a description dict.

    Parameters
    ----------
    description : dict
        Description of a dataset in xml dict.
    features : dict
        Description of a dataset features.
    qualities : list
        Description of a dataset qualities.
    arff_file : string, optional
        Path of dataset ARFF file.

    Returns
    -------
    dataset : dataset object
        Dataset object from dict and ARFF.
    """
    return ISMLLDataset(
        data_file=features,
        target_file = labels,
        folds=folds,
        validation_folds=validation_folds,
        dataset_id=dataset_id
    )
    
def _create_metadataset_from_description(
        dataset_id:int,
        metadataset: str,
) -> ISMLLMetaDataset:
    """Create a dataset object from a description dict.

    Parameters
    ----------
    description : dict
        Description of a dataset in xml dict.
    features : dict
        Description of a dataset features.
    qualities : list
        Description of a dataset qualities.
    arff_file : string, optional
        Path of dataset ARFF file.

    Returns
    -------
    dataset : dataset object
        Dataset object from dict and ARFF.
    """
    return ISMLLMetaDataset(
        metadata_file=metadataset,
        dataset_id=dataset_id
    )