import boto3
import time
import logging


class AWSDatabase(object):
    '''
    Configuration object for AWS RDS Database
    @author Jaap Gorjup
    '''

    logger = logging.getLogger('mm.awsrds.database')

    DEFAULT_ENGINE_NAME = 'postgresql'
    DEFAULT_ENGINE_VERSION = '12'
    DEFAULT_DB_INSTANCE_TYPE = 'm1.small'
    DEFAULT_DB_NAME = 'pg_db'
    DEFAULT_DB_USER_NAME = 'db_user'
    DEFAULT_DB_USER_PASSWORD = 'db_pass123'

    db_instance_name = 'test'
    db_instance_type = DEFAULT_DB_INSTANCE_TYPE
    db_engine = DEFAULT_ENGINE_NAME
    db_engine_version = DEFAULT_ENGINE_VERSION
    db_name = DEFAULT_DB_NAME
    db_master_username = DEFAULT_DB_USER_NAME

    def __init__(self, db_instance_name, aws_config):
        self.db_instance_name = db_instance_name
        self.rds_client = boto3.client("rds", config=aws_config)

    def check_if_exists():
        '''
        Checks if the database exists in AWS 
        Returns the ExternalName of the database server or False when absent
        '''
        return False

    def create(self,
               db_master_password,
               db_name=DEFAULT_DB_NAME,
               db_master_username=DEFAULT_DB_USER_NAME,
               db_instance_type=DEFAULT_DB_INSTANCE_TYPE,
               db_engine=DEFAULT_ENGINE_NAME,
               db_engine_version=DEFAULT_ENGINE_VERSION):

        # ------
        #  1. Create DB security group (if not exists else update)
        #  2. Create DB subnet group (name, vpc, az, subnets)

        db_param_grp_name = db_name + '_param_grp'
        db_param_grp_family = db_name + '_param_family'
        db_params_response = \
            self.rds_client.create_db_parameter_group(
                DBParameterGroupName=db_param_grp_name,
                DBParameterGroupFamily=db_param_grp_family,
                Description='%s DB Params Group' % self.db_instance_name)
        if db_params_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Created DB parameters group %s" % db_param_grp_name)
        else:
            print("Couldn't create DB parameters group")

        create_db_response = self.rds_client.create_db_instance(
            DBInstanceIdentifier=self.db_instance_name,
            DBInstanceClass=db_instance_type,
            DBName=db_name,
            Engine=db_engine,
            EngineVersion=db_engine_version,
            MasterUsername=db_master_username,
            MasterUserPassword=db_master_password,
            DBParameterGroupName=db_param_grp_name)
 
        if create_db_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Successfully create DB instance %s" % self.db_instance_name)
        else:
            print("Couldn't create DB instance")

    def delete(self):
        # Create DB snapshot
        db_snapshot_name = 'delete_snapshot_db'
        snapshot_response = self.rds_client.create_db_snapshot(
            DBInstanceIdentifier=self.db_instance_name,
            DBSnapshotIdentifier=db_snapshot_name)

        # check Create DB instance returned successfully
        if snapshot_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Successfully created snapshot %s" % self.db_instance_name)
        else:
            print("Couldn't create DB snapshot")

        print("waiting for snapshot %s to be ready" % self.db_instance_name)
        number_of_retries = 20
        snapshot_success = False

        for i in range(number_of_retries):
            time.sleep(30)
            snp_status = self.rds_client.describe_db_snapshots(
                DBSnapshotId=db_snapshot_name)['DBSnapshots'][0]['Status']
            if snp_status == 'available':
                snapshot_success = True
                print("DB snapshot %s is ready" % db_snapshot_name)
                break
            else:
                print("DB snapshot %s is initializing. Attempt %s" %
                      (db_snapshot_name, i))
        return snapshot_success
