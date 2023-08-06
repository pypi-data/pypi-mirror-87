import os
from pathlib import Path


DEBUG = os.environ.get('SAVVIHUB_DEBUG', False)
API_HOST = os.environ.get('SAVVIHUB_API_HOST', 'http://localhost:10000')
WEB_HOST = os.environ.get('SAVVIHUB_WEB_HOST', 'http://localhost:3000')

CUR_DIR = os.getcwd()
DEFAULT_SAVVI_DIR = os.path.join(str(Path.home()), '.savvihub')
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_SAVVI_DIR, 'config')

INQUIRER_NAME_IMAGE = 'image'
INQUIRER_NAME_RESOURCE = 'resource'
INQUIRER_NAME_DATASET = 'dataset'
INQUIRER_NAME_DATASET_REF = 'dataset_ref'
INQUIRER_NAME_DATASET_MOUNT_PATH = 'dataset_mount_path'
INQUIRER_NAME_COMMAND = 'command'

ROLETYPE_DATASET_FILES = 'dataset-files'
ROLETYPE_EXPERIMENT_OUTPUT = 'experiment-output'
ROLETYPE_EXPERIMENT_INPUT = 'experiment-input'

DATASET_SOURCE_TYPE_SAVVIHUB = 'savvihub'

DATASET_PATH_PARSE_SCHEME_GS = "gs"
DATASET_PATH_PARSE_SCHEME_S3 = "S3"
