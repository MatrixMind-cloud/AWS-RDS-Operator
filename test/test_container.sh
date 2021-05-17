#!/bin/bash

if [ -z "$KUBECONFIG" ]; then
    export KUBECONFIG="~/.kube/config"
fi

docker build -t mm/aws-rds-operator .
docker run -v $KUBECONFIG:/root/.kube/config mm/aws-rds-operator
