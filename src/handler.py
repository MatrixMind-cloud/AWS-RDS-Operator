import os
import kopf
import logging
# import random
import time
# import sys
import boto3
import botocore
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

rds_client = boto3.client("rds",
                          config=my_config)


@kopf.on.event('', 'v1', 'mm-rds')
async def my_handler(spec, **_):
    '''
    Handlers for RDS database object events in Kubernetes.
    '''
    logger.info('Generic event detected')


@kopf.on.create('', 'v1', 'mm-rds')
def my_update_handler(spec, **_):
    logger.info('Create database detected')

    #  Get parameters from CRD
    db_instance_name = 'test'
    db_instance_type = 'default'
    db_engine = 'postgres'
    db_engine_version = '13'
    db_name = 'test'
    db_master_username = 'root'
    #  Check if database already exists, if is, communicate error and skip
    #  else create database
    #  generate secrets
    db_master_password = 'rootroot'
    # ------
    #  1. Create DB security group (if not exists else update)
    #  2. Create DB subnet group (name, vpc, az, subnets)
    #  3. Create DB Parameter Group (if not exists)
    db_param_grp_name = db_name + '_param_grp'
    db_param_grp_family = db_name + '_param_family'
    create_db_params_response = \
        rds_client.create_db_parameter_group(
            DBParameterGroupName=db_param_grp_name,
            DBParameterGroupFamily=db_param_grp_family,
            Description='%s DB Params Group' % db_instance_name)
    if create_db_params_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Created DB parameters group %s" % db_param_grp_name)
    else:
        print("Couldn't create DB parameters group")
    # TODO report status

    #  4. Create DB Instance
    create_db_response = rds_client.create_db_instance(
        DBInstanceIdentifier=db_instance_name,
        DBInstanceClass=db_instance_type,
        DBName=db_name,
        Engine=db_engine,
        EngineVersion=db_engine_version,
        MasterUsername=db_master_username,
        MasterUserPassword=db_master_password,
        DBParameterGroupName=db_param_grp_name)

    if create_db_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Successfully create DB instance %s" % db_instance_name)
    else:
        print("Couldn't create DB instance")

    # Wait for database to be available

    # -----------
    #  When ready store parameters as secret in same namespace
    # 
    #  Optional create 'local' service reference to externalName :
# apiVersion: v1
# kind: Service
# metadata:
#   name: mysql
# spec:
#   type: ExternalName
#   externalName: usermgmtdb.c7hldelt9xfp.us-east-1.rds.amazonaws.com

    # Postconfig
    # 1. Store root account in secret in same namespace
    # 2. Connect to DB using master settings
    # 3. Create database schema and accounts (with roles)
    # 4. Create per account secret with username and password


@kopf.on.delete('', 'v1', 'mm-rds')
def my_delete_handler(spec, **_):
    logger.info('Delete database detected')

# Create DB snapshot
    db_instance_name = 'test'
    db_snapshot_name = 'delete_snapshot_db'
    create_db_snapshot_response = rds_client.create_db_snapshot(
        DBInstanceIdentifier=db_instance_name,
        DBSnapshotIdentifier=db_snapshot_name)

    # check Create DB instance returned successfully
    if create_db_snapshot_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Successfully created DB snapshot %s" % db_instance_name)
    else:
        print("Couldn't create DB snapshot")

    print("waiting for db snapshot %s to become ready" % db_instance_name)
    number_of_retries = 20
    snapshot_success = False
    for i in xrange(number_of_retries):
        time.sleep(30)
        snp_status = rds_client.describe_db_snapshots(
            DBSnapshotIdentifier=db_snapshot_name)['DBSnapshots'][0]['Status']
        if snp_status == 'available':
            snapshot_success = True
            print("DB snapshot %s is ready" % db_snapshot_name)
            break
        else:
            print("DB snapshot %s is initializing. Attempt %s" %
                  (db_snapshot_name, i))


def generate_unique_passsword():
    '''
    Unique password generator based on hash complexity generator settings
    '''
    # TODO create pasword generator
    return "unique"


def create_secret(database, username, password):
    return ''


'''
Nice initialization header
'''
print('')
custom_fig = Figlet(font='graffiti')
print(custom_fig.renderText('Matrixmind'))
print("Project: AWS RDS Operator")
print("--------------------------------------")
