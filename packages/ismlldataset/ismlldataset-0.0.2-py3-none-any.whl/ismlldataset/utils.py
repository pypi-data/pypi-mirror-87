import os
import shutil

from . import config
import zipfile
import wget
def _create_cache_directory(key):
    cache = config.get_cache_directory()
    cache_dir = os.path.join(cache, key)
    try:
        os.makedirs(cache_dir)
    except OSError:
        pass
    return cache_dir


def _create_cache_directory_for_id(key, id_):
    """Create the cache directory for a specific ID

    In order to have a clearer cache structure and because every task
    is cached in several files (description, split), there
    is a directory for each task witch the task ID being the directory
    name. This function creates this cache directory.

    This function is NOT thread/multiprocessing safe.

    Parameters
    ----------
    key : str

    id_ : int

    Returns
    -------
    str
        Path of the created dataset cache directory.
    """
    cache_dir = os.path.join(
        _create_cache_directory(key), str(id_)
    )
    if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
        pass
    elif os.path.exists(cache_dir) and not os.path.isdir(cache_dir):
        raise ValueError('%s cache dir exists but is not a directory!' % key)
    else:
        os.makedirs(cache_dir)
    return cache_dir


def _remove_cache_dir_for_id(key, cache_dir):
    """Remove the task cache directory

    This function is NOT thread/multiprocessing safe.

    Parameters
    ----------
    key : str

    cache_dir : str
    """
    try:
        shutil.rmtree(cache_dir)
    except (OSError, IOError):
        raise ValueError('Cannot remove faulty %s cache directory %s.'
                         'Please do this manually!' % (key, cache_dir))

def _download_zip_file(source: str,
                        output_path: str,
                        exists_ok: bool = True,
                        encoding: str = 'utf8',
                        ) -> None:
    """ Download the text file at `source` and store it in `output_path`.

    By default, do nothing if a file already exists in `output_path`.
    The downloaded file can be checked against an expected md5 checksum.

    Parameters
    ----------
    source : str
        url of the file to be downloaded
    output_path : str
        full path, including filename, of where the file should be stored.
    md5_checksum : str, optional (default=None)
        If not None, should be a string of hexidecimal digits of the expected digest value.
    exists_ok : bool, optional (default=True)
        If False, raise an FileExistsError if there already exists a file at `output_path`.
    encoding : str, optional (default='utf8')
        The encoding with which the file should be stored.
    """
    local_file=os.path.join(output_path,source.split('/')[-1])
    # config.oc.get_file(source,local_file=local_file)
    wget.download(url=source,out=local_file)

    # Create a ZipFile Object and load sample.zip in it
    with zipfile.ZipFile(local_file, 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall(path=output_path)
       print('dataset downloaded')
#    with open(output_path, "w", encoding=encoding) as fh:
#        fh.write(downloaded_file)

    os.remove(local_file)