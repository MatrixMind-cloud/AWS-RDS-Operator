import os
import kopf
import logging
import time

from database import AWSDatabase
from k8s import DatabaseSecret

from botocore.config import Config

from pyfiglet import Figlet

'''
Variables that can be set using environment and defaults
'''
DEVELOPMENT = os.environ.get('DEVELOPMENT', 'False').lower() == 'true'
K8S_SSL_VERIFY = bool(os.environ.get('K8S_SSL_VERIFY', 'False'))

AWS_REGION = os.environ.get('AWS_REGION', 'eu-central-1')
AWS_ACCESS = os.environ.get('AWS_ACCESS', '')
AWS_SECRET = os.environ.get('AWS_SECRET', '')

'''
Default logger scope
'''
logger = logging.getLogger('mm.awsrds.controller')

# TODO initialize based on config with keys or without for Kube2IAM
# TODO place these in a class wrapper
my_config = Config(
    region_name=AWS_REGION,
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)
# TODO add these to config if not empty
#   aws_access_key_id=AWS_ACCESS,
#   aws_secret_access_key=AWS_SECRET

# During init : detect cloud or check parameters (development)


@kopf.on.resume('', 'v1', 'rdsdatabases')
@kopf.on.create('', 'v1', 'rdsdatabases')
def my_create_handler(spec,  name, namespace, logger, **kwargs):
    logger.info('Create database detected')
    logger.debug(spec)

    # input checking
    size = spec.get('size')
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

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


@kopf.on.update('', 'v1', 'rdsdatabases')
def my_update_handler(spec, old, new, diff, **_):
    # Input check
    # Find RDS database
    # Update value
    pass


@kopf.on.delete('', 'v1', 'rdsdatabases')
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
