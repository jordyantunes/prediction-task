# /bin/bash 
ENV="dev"
K8S_NAMESPACE="default"
DEPLOY_DIR="deploy"

export $(grep -v '^#' configs/$ENV.env | xargs)

echo "Deploying to Kubernetes environment: $ENV"
kubectl apply -f $DEPLOY_DIR/$ENV/deployment.yaml
kubectl apply -f $DEPLOY_DIR/$ENV/service.yaml
kubectl apply -f $DEPLOY_DIR/$ENV/ingress.yaml

echo "Deployment complete."