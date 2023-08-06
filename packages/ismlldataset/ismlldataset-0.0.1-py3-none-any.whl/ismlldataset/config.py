"""
Store module level information like the API key, cache directory and the server
"""
import logging
import os
# import owncloud
from io import StringIO
import configparser
from urllib.parse import urlparse


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s:%(name)s] %('
           'message)s', datefmt='%H:%M:%S')

# Default values!
_defaults = {
    'server': "https://www.ismll.uni-hildesheim.de/personen/hsjomaa/",
    'verbosity': 0,
    'cachedir': os.path.expanduser(os.path.join('~', '.ismll', 'cache')),
    'avoid_duplicate_runs': 'True',
    'connection_n_retries': 2,
}

config_file = os.path.expanduser(os.path.join('~', '.ismll', 'config'))

# Default values are actually added here in the _setup() function which is
# called at the end of this module
# server   = _defaults['server']
# username = _defaults['username']
# password = _defaults['password']
# oc = owncloud.Client(server)
# oc.login(username,password)
# The current cache directory (without the server name)
cache_directory = _defaults['cachedir']
avoid_duplicate_runs = True if _defaults['avoid_duplicate_runs'] == 'True' else False

# Number of retries if the connection breaks
connection_n_retries = _defaults['connection_n_retries']


def _setup():
    """Setup ismll package. Called on first import.

    Reads the config file and sets up apikey, server, cache appropriately.
    key and server can be set by the user simply using
    ismll.config.apikey = THEIRKEY
    ismll.config.server = SOMESERVER
    We could also make it a property but that's less clear.
    """
    global server
    global cache_directory
    global avoid_duplicate_runs
    global connection_n_retries
    # read config file, create cache directory
    try:
        os.mkdir(os.path.expanduser(os.path.join('~', '.ismll')))
    except (IOError, OSError):
        # TODO add debug information
        pass
    config = _parse_config()
    server = config.get('FAKE_SECTION', 'server')

    short_cache_dir = config.get('FAKE_SECTION', 'cachedir')
    cache_directory = os.path.expanduser(short_cache_dir)

    avoid_duplicate_runs = config.getboolean('FAKE_SECTION',
                                             'avoid_duplicate_runs')
    connection_n_retries = config.get('FAKE_SECTION', 'connection_n_retries')
    if connection_n_retries > 20:
        raise ValueError(
            'A higher number of retries than 20 is not allowed to keep the '
            'server load reasonable'
        )


def _parse_config():
    """Parse the config file, set up defaults.
    """

    config = configparser.RawConfigParser(defaults=_defaults)

    if not os.path.exists(config_file):
        # Create an empty config file if there was none so far
        fh = open(config_file, "w")
        fh.close()
        logger.info("Could not find a configuration file at %s. Going to "
                    "create an empty file there." % config_file)

    try:
        # Cheat the ConfigParser module by adding a fake section header
        config_file_ = StringIO()
        config_file_.write("[FAKE_SECTION]\n")
        with open(config_file) as fh:
            for line in fh:
                config_file_.write(line)
        config_file_.seek(0)
        config.read_file(config_file_)
    except OSError as e:
        logging.info("Error opening file %s: %s", config_file, e.message)
    return config

def get_local_directory():
    """Get the local dataset directory.

    Returns
    -------
    cachedir : string
        The local dataset directory.

    """
    _datasetdir = '/home/hsjomaa/cross_task_surrogate_learning/data/repo/origin/'
    return _datasetdir

def get_cache_directory():
    """Get the current cache directory.

    Returns
    -------
    cachedir : string
        The current cache directory.

    """
    url_suffix = urlparse(server).netloc
    reversed_url_suffix = os.sep.join(url_suffix.split('.')[::-1])
    if not cache_directory:
        _cachedir = _defaults(cache_directory)
    else:
        _cachedir = cache_directory
    _cachedir = os.path.join(_cachedir, reversed_url_suffix)
    return _cachedir


def set_cache_directory(cachedir):
    """Set module-wide cache directory.

    Sets the cache directory into which to download datasets, tasks etc.

    Parameters
    ----------
    cachedir : string
         Path to use as cache directory.

    See also
    --------
    get_cache_directory
    """

    global cache_directory
    cache_directory = cachedir


__all__ = [
    'get_cache_directory', 'set_cache_directory'
]

_setup()

def _get_dataset_url(dataset_id:int):
    if dataset_id in list(_map.keys()):
        return f"{server}{dataset_id}.zip"
    else:
        return None
    
_map = {0: 'oocytes_trisopterus_states_5b',
 1: 'pittsburg-bridges-SPAN',
 2: 'statlog-heart',
 3: 'molec-biol-promoter',
 4: 'yeast',
 5: 'monks-3',
 6: 'titanic',
 7: 'synthetic-control',
 8: 'ionosphere',
 9: 'pittsburg-bridges-T-OR-D',
 10: 'breast-tissue',
 11: 'ecoli',
 12: 'oocytes_merluccius_nucleus_4d',
 13: 'plant-margin',
 14: 'conn-bench-vowel-deterding',
 15: 'optical',
 16: 'magic',
 17: 'miniboone',
 18: 'heart-switzerland',
 19: 'breast-cancer-wisc-prog',
 20: 'ringnorm',
 21: 'lung-cancer',
 22: 'steel-plates',
 23: 'plant-shape',
 24: 'echocardiogram',
 25: 'lymphography',
 26: 'energy-y2',
 27: 'musk-1',
 28: 'plant-texture',
 29: 'statlog-australian-credit',
 30: 'vertebral-column-2clases',
 31: 'abalone',
 32: 'blood',
 33: 'credit-approval',
 34: 'molec-biol-splice',
 35: 'wine-quality-white',
 36: 'bank',
 37: 'car',
 38: 'low-res-spect',
 39: 'horse-colic',
 40: 'hill-valley',
 41: 'statlog-shuttle',
 42: 'hayes-roth',
 43: 'cardiotocography-3clases',
 44: 'breast-cancer-wisc',
 45: 'adult',
 46: 'glass',
 47: 'fertility',
 48: 'mammographic',
 49: 'statlog-german-credit',
 50: 'oocytes_merluccius_states_2f',
 51: 'congressional-voting',
 52: 'soybean',
 53: 'planning',
 54: 'pittsburg-bridges-MATERIAL',
 55: 'statlog-vehicle',
 56: 'zoo',
 57: 'arrhythmia',
 58: 'lenses',
 59: 'ozone',
 60: 'seeds',
 61: 'cylinder-bands',
 62: 'wine',
 63: 'tic-tac-toe',
 64: 'acute-nephritis',
 65: 'connect-4',
 66: 'pima',
 67: 'statlog-image',
 68: 'chess-krvkp',
 69: 'musk-2',
 70: 'waveform',
 71: 'flags',
 72: 'wall-following',
 73: 'pendigits',
 74: 'iris',
 75: 'cardiotocography-10clases',
 76: 'statlog-landsat',
 77: 'twonorm',
 78: 'heart-cleveland',
 79: 'primary-tumor',
 80: 'oocytes_trisopterus_nucleus_2f',
 81: 'post-operative',
 82: 'spect',
 83: 'acute-inflammation',
 84: 'chess-krvk',
 85: 'dermatology',
 86: 'libras',
 87: 'mushroom',
 88: 'parkinsons',
 89: 'waveform-noise',
 90: 'heart-hungarian',
 91: 'heart-va',
 92: 'audiology-std',
 93: 'haberman-survival',
 94: 'energy-y1',
 95: 'page-blocks',
 96: 'conn-bench-sonar-mines-rocks',
 97: 'semeion',
 98: 'hepatitis',
 99: 'contrac',
 100: 'led-display',
 101: 'breast-cancer-wisc-diag',
 102: 'vertebral-column-3clases',
 103: 'ilpd-indian-liver',
 104: 'monks-1',
 105: 'image-segmentation',
 106: 'pittsburg-bridges-TYPE',
 107: 'thyroid',
 108: 'nursery',
 109: 'wine-quality-red',
 110: 'breast-cancer',
 111: 'letter',
 112: 'pittsburg-bridges-REL-L',
 113: 'monks-2',
 114: 'balloons',
 115: 'spectf',
 116: 'balance-scale',
 117: 'teaching',
 118: 'spambase',
 119: 'annealing'}