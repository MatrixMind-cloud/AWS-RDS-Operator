#!/bin/bash

# Check if local K8S cluster is available
command kubectl cluster-info >/dev/null 2>&1
if [ "$?" -eq 127 ];  then
    echo "Kubectl utility not installed, exiting"
    exit
fi

# Check if kopf is available or else install it
if ! command -v kopf &> /dev/null
then
    echo "Kopf could not be found locally ... installing it now with pip"
    pip install kopf
fi

# Check if the CRD is available in Kubernetes or else load it
crd_check=$(kubectl get crd -o name 2>&1)
if [[ $crd_check =~ "refused" ]]; then
     echo "Could not connect to cluster, exiting"
     exit
else 
    # TODO add the check for the CRD here
    if [[ $crd_check =~ "pizza" ]]; then
        echo "Loading CRD in Kubernetes cluster"
        kubectl apply -f helm/aws-rds-operator/templates/crd.yaml
    fi
fi

# Start
kopf run src/handler.py 