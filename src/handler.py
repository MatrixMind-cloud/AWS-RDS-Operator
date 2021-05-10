import os
import kopf
import pykube
import logging
import requests

from pyfiglet import Figlet

'''
Variables that can be set using environment and defaults
'''
DEVELOPMENT = os.environ.get('DEVELOPMENT', 'False').lower() == 'true'
K8S_SSL_VERIFY = bool(os.environ.get('K8S_SSL_VERIFY', 'False'))

'''
Default logger scope
'''
logger = logging.getLogger('mm.awsrds.controller')


@kopf.on.event('', 'v1', 'mm-rds')
async def my_handler(spec, **_):
    '''
    Handlers for RDS database object events in Kubernetes.
    '''
    logger.info('Generic event detected')


@kopf.on.create('', 'v1', 'mm-rds')
def my_update_handler(spec, **_):
    logger.info('Create database detected')


@kopf.on.delete('', 'v1', 'mm-rds')
def my_delete_handler(spec, **_):
    logger.info('Delete database detected')


'''
Nice initialization header
'''
print('')
custom_fig = Figlet(font='graffiti')
print(custom_fig.renderText('Matrixmind'))
print("Project: AWS RDS Operator")
print("--------------------------------------")
