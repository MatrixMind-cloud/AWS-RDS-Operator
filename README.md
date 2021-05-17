# AWS-RDS-Operator

[![build](https://github.com/MatrixMind-cloud/AWS-RDS-Operator/actions/workflows/main.yml/badge.svg)](https://github.com/MatrixMind-cloud/AWS-RDS-Operator/actions/workflows/main.yml)

## Local test

In order to run it on your machine ensure you need to have a connection to a Kubernetes cluster.
It will use the default KUBECONFIG setting or `~/.kube/config` file for connecting.

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

Needed to get into alpha phase:

- [x] Docker container building in Github
- [x] Finalize CRD yaml according to spec in README
- [ ] AWS access code initializer
- [ ] Code on.create handler using the k8s and rds tooling
- [ ] Code on.update handler determining the difference either size or users
- [ ] Code on.delete handler removing service and starting snapshot. Secrets stay.
- [ ] Database access checker component needed
- [ ] Error handling and logging of the Operator

Additional nice to haves:

- [ ] Minimization of Docker container size through Dockerslim
- [ ] Add support for MySQL
- [ ] Cross cloud support (Azure, GCP)
- [ ] On premise fallback option using another operator (configurable)
- [ ] Status logging in objects equal to cloud status
- [ ] Object log retrieval equal to log of database in cloud
- [ ] Configurable backup support including offload to cold storage
- [ ] Supporting multiple replicas (mapped to AZ of the cluster)
