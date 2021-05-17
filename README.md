# AWS-RDS-Operator

[![build](https://github.com/MatrixMind-cloud/AWS-RDS-Operator/actions/workflows/main.yml/badge.svg)](https://github.com/MatrixMind-cloud/AWS-RDS-Operator/actions/workflows/main.yml)

## Local test

In order to run it on your machine ensure you need to have a connection to a Kubernetes cluster.
It will use the default KUBECONFIG setting or `~/.kube/config` file for connecting.

Ensure proper AWS credentials are set as environment variables:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

Starting can be done using the command:

```bash
local.sh
```

## Kubernetes syntax

``` yaml
apiVersion: matrixmind.cloud/v1 
kind: RDSDatabase
metadata: 
    name: databasename
    namespace: namespacename
spec:
    type: Postgresql|MySQL (postgres default)
    version: optional version number (12 default)
    size: 10GB (default)
    masteruser: sysadmin (default)
    users:
      username1: 
        - superuser
        - createdb
      username2: []
    databases:
      database1: 
        - username1
        - username2
      database2: 
        - username1
    backup:
        every: 24h (default)
        retention: 7d (default)
```

By default if nothing is filled in the spec: part a 10GB Postgresql version 12 with master user sysadmin is created.
Optionally separate users and databases can be added. Per database users and roles can be mapped.

After successful registration of the RDSDatabase in the namespace, the following will be added:

- service object with the name : [name].rds.svc
- secret for the master user with username and password : [name].rds.master
- secret per user created : [name].rds.[username]

The applications can bind to the database using the service object and using the secret.
The secret data is added immediately since creation of the RDS can take a while.
The service is only added when the RDS is ready.

## Status

Project is still WIP and is an aside project.

**Needed to get into alpha phase:**

- [x] Docker container building in Github
- [x] Finalize CRD yaml according to spec in README
- [x] AWS access code initializer --> Standard Boto environment variables (https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#environment-variables)
- [ ] Secret initializer for accounts and passwords
- [~] Code on.create handler using the k8s and rds tooling
- [ ] Code on.update handler determining the difference either size or users
- [ ] Code on.delete handler removing service and starting snapshot. Secrets stay.
- [ ] Database access checker component needed
- [ ] Error handling and logging of the Operator
- [ ] Validate Kube2IAM integration and add support in Helm chart for this

**Additional nice to haves:**

- [ ] Minimization of Docker container size through Dockerslim
- [ ] Allowing encryotion to be defined generically and per yamml
- [ ] Add support for MySQL
- [ ] Add support for Aurora variants
- [ ] Cross cloud support (Azure, GCP)
- [ ] On premise fallback option using another operator (configurable)
- [ ] Status logging in objects equal to cloud status
- [ ] Object log retrieval equal to log of database in cloud
- [ ] Configurable backup support including offload to cold storage
- [ ] Supporting multiple replicas (mapped to AZ of the cluster)
- [ ] Regular verification of status of datbase through cron in Kopf

## Remarks

Local development testing will have a visible error during startup because it will try to authenticate to the Kubernetes cluster using service account token. This error message can be ignored:

```text
kopf.activities.auth [ERROR   ] Activity 'login_via_pykube' failed with an exception. Will ignore.
Traceback (most recent call last):
  File "/Users/xyz/.pyenv/versions/3.8.2/lib/python3.8/site-packages/kopf/utilities/piggybacking.py", line 93, in login_via_pykube
    config = pykube.KubeConfig.from_service_account()
  File "/Users/xyz/.pyenv/versions/3.8.2/lib/python3.8/site-packages/pykube/config.py", line 22, in from_service_account
    with open(os.path.join(path, "token")) as fp:
FileNotFoundError: [Errno 2] No such file or directory: '/var/run/secrets/kubernetes.io/serviceaccount/token'
```
