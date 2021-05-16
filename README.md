# AWS-RDS-Operator
## Local test

In order to run it on your machine ensure you need to have a connection to a Kubernetes cluster.
It will use the default KUBECONFIG setting or `~/.kube/config` file for connecting.

Starting can be done using the command:

```bash
local.sh
```


## Kubernetes syntax

``` yaml
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
    - username1
    - username2
    databases:
    - database1:
        - user: username1
          role: admin
        - user: username1
          role: user
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