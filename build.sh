# /bin/bash
ENV="dev"
TAG="latest"

echo "Loading environment variables from configs/$ENV.env"
export $(grep -v '^#' configs/$ENV.env | xargs)

echo "Building Docker image..."
docker build -f build/Dockerfile -t $IMAGE_NAME:$TAG .

echo "Build and push complete."
docker tag $IMAGE_NAME $DOCKER_REGISTRY/$IMAGE_NAME:$TAG
docker push $DOCKER_REGISTRY/$IMAGE_NAME:$TAG