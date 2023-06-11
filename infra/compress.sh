#!/bin/bash

cd lambda
pip install --target ./packages pandas pyarrow
cd packages
zip -r ../source.zip .
cd .. && zip source.zip lambda.py