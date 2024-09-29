# /bin/bash 
ENV="dev"
K8S_NAMESPACE="default"
CHART_DIR="./chart/"

export $(grep -v '^#' configs/$ENV.env | xargs)

echo "Deploying to Kubernetes environment: $ENV"
helm upgrade --install predict-deploy $CHART_DIR \
    --namespace $K8S_NAMESPACE \
    --set image.repository=$DOCKER_REGISTRY/$IMAGE_NAME \
    --set image.tag=$TAG \
    --set image.pullPolicy=Always

echo "Deployment complete."