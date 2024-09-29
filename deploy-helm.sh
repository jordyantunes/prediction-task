# /bin/bash 
ENV="dev"
K8S_NAMESPACE="default"
CHART_DIR="./chart/"

export $(grep -v '^#' configs/$ENV.env | xargs)

echo "Deploying to Kubernetes environment: $ENV"
helm install predict-deploy $CHART_DIR

echo "Deployment complete."