#!/bin/bash

cd lambda
pip install --target ./packages pyarrow
cd packages
zip -r ../source.zip .
cd .. && zip source.zip lambda.py