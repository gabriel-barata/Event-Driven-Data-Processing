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
    cd ..

}

run() {

    echo "Runing python app..."
    
    cd infra
    bucket_name=$(terraform output -raw bucket-name)
    export BUCKET_NAME=$bucket_name
    cd ..

    cd app
    python3 main.py

}

destroy() {

    cd infra
    terraform destroy -auto-approve
    cd ..

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
            echo "-e: No argument was declared! Usage: $0 {deploy | run | destroy}"
        else
            echo "-e: Invalid Argument! Usage: $0 {deploy | run | destroy}"
        fi
    ;;
esac
