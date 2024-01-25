#!/usr/bin/env bash

deploy(){

    # Generating the .zip with dependencies for Lambda func
    cd infra && chmod +x compress.sh
    echo "Compressing Lambda dependencies..."
    ./compress.sh
    # Seting AWS resources up
    echo "Deploying AWS resources..."
    terraform init
    terraform plan && terraform apply -auto-approve
    bucket_name=$(terraform output -raw aws_s3_bucket.s3-bucket[0].id)
    export BUCKET_NAME=$bucket_name
    cd ..

}

run() {

    echo "Runing python app..."
    cd app
    python3 main.py

}

destroy() {

    cd infra
    terraform destroy -auto-approve
    cd ..
    unset BUCKET_NAME

}

case $1 in 
    deploy | DEPLOY)
        deploy
        ;;
    run | RUN)
        run
        ;;
    destroy | DESTROY)
        destroy
        ;;
    *)
        if [ $# -eq 0 ]; then
            echo "-e: No argument was delceared! Usage: $0 {deploy | run | destroy}"
            ;;
        else
            echo "-e: Invalid Argument! Usage: $0 {deploy | run | destroy}"
esac