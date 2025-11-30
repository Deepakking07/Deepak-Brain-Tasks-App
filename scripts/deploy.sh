#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting deployment to EKS cluster..."

# --- Paths ---
AWS="/opt/bin/aws"
KUBECTL="/tmp/app/kubectl"
KUBECONFIG="/tmp/.kube/config"

# --- Ensure directory exists ---
mkdir -p $(dirname $KUBECONFIG)

# --- Update kubeconfig for EKS cluster ---
echo "📝 Updating kubeconfig..."
$AWS eks update-kubeconfig --region ap-south-1 --name brain-task-cluster --kubeconfig $KUBECONFIG

# --- Apply Kubernetes manifests ---
echo "⚙️  Applying deployment manifest..."
$KUBECTL --kubeconfig $KUBECONFIG apply --validate=false -f /tmp/app/deployment.yaml

echo "⚙️  Applying service manifest..."
$KUBECTL --kubeconfig $KUBECONFIG apply --validate=false -f /tmp/app/service.yaml

# --- Verify deployment ---
echo "🔍 Verifying deployment status..."
$KUBECTL --kubeconfig $KUBECONFIG get deployments
$KUBECTL --kubeconfig $KUBECONFIG get pods
$KUBECTL --kubeconfig $KUBECONFIG get services

echo "🎉 Deployment completed successfully!"
