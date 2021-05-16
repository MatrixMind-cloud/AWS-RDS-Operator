from kubernetes import client, config
import logging


class DatabaseSecret(object):
    '''
    Utility class to manage usernames and passwords for databases stored in K8s
    @author Jaap Gorjup
    '''

    logger = logging.getLogger('mm.awsrds.k8s')

    def __init__(name, namespace, username=None, password=None):
        '''
        Setup interaction with Kubernetes
        Check if secret exists and if not create it
        '''
        pass

    def __create_secret(name, namespace):
        pass

    def __load_secret(name, namespace):
        pass

    def generate_unique_passsword():
        '''
        Unique password generator based on hash complexity generator settings
        '''
        # TODO create pasword generator
        return "unique"

    def get_username():
        return ""

    def get_password():
        return ""


class DatabaseService(object):
    '''
    Utility class to make database service available as a K8s service
    @author Jaap Gorjup

apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  type: ExternalName
  externalName: usermgmtdb.c7hldelt9xfp.us-east-1.rds.amazonaws.com
    '''

    logger = logging.getLogger('mm.awsrds.k8s')

    def __init__(name, namespace, externalname):
        '''
        Setup interaction with Kubernetes
        Check if secret exists and if not create it
        '''
        pass
