#!/bin/bash

if ! command -v kopf &> /dev/null
then
    echo "kopf could not be found locally ... installing it now with pip"
    pip install kopf
fi

kopf run src/handler.py 