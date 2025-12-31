#/bin/bash

container_ids=$(docker ps -a | awk '$2 == "backend.mywebapp.local" {print $1}')
if [ -n "$container_ids" ]; then
        for id in $container_ids; do
                echo "removing  my-web-app-backend:latest $id"
                docker rm  "$id"
        done
fi

container_ids=$(docker ps -a | awk '$2 == "my-web-app-frontend:latest" {print $1}')
if [ -n "$container_ids" ]; then
        for id in $container_ids; do
                echo "removing my-web-app-frontend:latest $id"
                docker rm  "$id"
        done
fi

cd ../..
docker-compose -f docker-compose-oci.yml up