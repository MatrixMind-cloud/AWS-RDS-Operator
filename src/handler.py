import os
import kopf
import logging

from database import AWSDatabase
from k8s import DatabaseSecret

from botocore.config import Config

from pyfiglet import Figlet

'''
Variables that can be set using environment and defaults
'''
DEVELOPMENT = os.environ.get('DEVELOPMENT', 'False').lower() == 'true'
K8S_SSL_VERIFY = bool(os.environ.get('K8S_SSL_VERIFY', 'False'))
DRY_RUN = bool(os.environ.get('K8S_SSL_VERIFY', 'False'))

'''
Default logger scope
'''
logger = logging.getLogger('mm.awsrds.controller')

my_config = Config(
    region_name=os.environ.get('AWS_REGION', 'eu-central-1'),
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)


@kopf.on.resume('matrixmind.cloud', 'v1', 'RDSDatabase')
@kopf.on.create('matrixmind.cloud', 'v1', 'RDSDatabase')
def my_create_handler(spec,  name, namespace, logger, **kwargs):
    logger.info('Create database detected')
    logger.debug(spec)

    # input checking
    size = spec.get('size', '10G')
    version = spec.get('version', '12')
    masteruser = spec.get('masteruser','sysadmin')

    # create secret for masteruser and get password

    database = AWSDatabase(name, my_config)
    if not database.exists():
        database.create('test123', name, masteruser)

    # if not size:
    #     raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    # Waiting for database ready error
    # if not is_data_ready():
    #    raise kopf.TemporaryError("The data is not yet ready.", delay=60)
        
    # 1. Create or load secrets
    # 2. Create database

    # Postconfig
    # 1. Store root account in secret in same namespace
    # 2. Connect to DB using master settings
    # 3. Create database schema and accounts (with roles)
    # 4. Create per account secret with username and password


@kopf.on.update('matrixmind.cloud', 'v1', 'RDSDatabase')
def my_update_handler(spec, old, new, diff, **_):
    # Input check
    # Find RDS database
    # Update value
    pass


@kopf.on.delete('matrixmind.cloud', 'v1', 'RDSDatabase')
def my_delete_handler(spec, **_):
    logger.info('Delete database detected')
    # 1. Start snapshot 
    # 2. Check if DELETE_PROTECTION is enabled
    # 3. If not enable delete database
    # 4. Delete service
    pass


'''
Nice initialization header
'''
print('')
custom_fig = Figlet(font='graffiti')
print(custom_fig.renderText('Matrixmind'))
print("Project: Cloud Database Operator")
print("--------------------------------------")
