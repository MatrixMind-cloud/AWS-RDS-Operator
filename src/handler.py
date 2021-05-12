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

# TODO most variables come from comfig so these should be env defaults
DEFAULT_ENGINE_NAME = 'postgresql'
DEFAULT_ENGINE_VERSION = ''
DEFAULT_DB_INSTANCE_TYPE = 'm1.small'
DEFAULT_DB_NAME = 'pg_db'
DEFAULT_DB_USER_NAME = 'db_user'
DEFAULT_DB_USER_PASSWORD = 'db_pass123'

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


@kopf.on.event('', 'v1', 'mm-rds')
async def my_handler(spec, **_):
    '''
    Handlers for RDS database object events in Kubernetes.
    '''
    logger.info('Generic event detected')


@kopf.on.create('', 'v1', 'mm-rds')
def my_update_handler(spec, **_):
    logger.info('Create database detected')

    # 1. Create or load secrets
    # 2. Create database

    # Postconfig
    # 1. Store root account in secret in same namespace
    # 2. Connect to DB using master settings
    # 3. Create database schema and accounts (with roles)
    # 4. Create per account secret with username and password


@kopf.on.delete('', 'v1', 'mm-rds')
def my_delete_handler(spec, **_):
    logger.info('Delete database detected')
    pass


'''
Nice initialization header
'''
print('')
custom_fig = Figlet(font='graffiti')
print(custom_fig.renderText('Matrixmind'))
print("Project: AWS RDS Operator")
print("--------------------------------------")
