#/bin/bash

BACKEND_CONTAINER_NAME="backend.mywebapp.local"

# Check if the container is running
if docker ps --format '{{.Names}}' | grep -wq "$BACKEND_CONTAINER_NAME"; then
    echo "Container '$BACKEND_CONTAINER_NAME' is running. Stopping it..."
    docker stop "$BACKEND_CONTAINER_NAME"
    echo "Container '$BACKEND_CONTAINER_NAME' stopped."
else
    echo "Container '$BACKEND_CONTAINER_NAME' is not running."
fi

FRONTEND_CONTAINER_NAME="my-web-app-frontend"

# Check if the container is running
if docker ps --format '{{.Names}}' | grep -wq "$FRONTEND_CONTAINER_NAME"; then
    echo "Container '$FRONTEND_CONTAINER_NAME' is running. Stopping it..."
    docker stop "$FRONTEND_CONTAINER_NAME"
    echo "Container '$FRONTEND_CONTAINER_NAME' stopped."
else
    echo "Container '$FRONTEND_CONTAINER_NAME' is not running."
fi


container_ids=$(docker ps -a | awk -v name="$BACKEND_CONTAINER_NAME" '$NF == name {print $1}')
if [ -n "$container_ids" ]; then
        for id in $container_ids; do
                echo "removing $BACKEND_CONTAINER_NAME $id"
                docker rm  "$id"
        done
fi

container_ids=$(docker ps -a | awk -v name="$FRONTEND_CONTAINER_NAME" '$NF == name {print $1}')
if [ -n "$container_ids" ]; then
        for id in $container_ids; do
                echo "removing $FRONTEND_CONTAINER_NAME $id"
                docker rm  "$id"
        done
fi

cd ~/my-web-app/
git pull

echo "Build frontend"
docker build -f Dockerfile-frontend -t my-web-app-frontend:latest .

echo "Build backend"
docker build -f Dockerfile-backend -t my-web-app-backend:latest .