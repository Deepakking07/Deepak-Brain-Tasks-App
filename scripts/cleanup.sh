#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# --- Paths for Lambda ---
AWS="/opt/bin/aws"         # AWS CLI path from Lambda layer
KUBECTL="/tmp/app/kubectl" # kubectl binary from deployment package
KUBECONFIG="/tmp/.kube/config" # Temporary kubeconfig location

# --- Ensure tmp .kube directory exists ---
mkdir -p $(dirname $KUBECONFIG)

echo "🧹 Cleaning up old deployment (if exists)..."
$KUBECTL --kubeconfig $KUBECONFIG delete -f /tmp/app/deployment.yaml --ignore-not-found || true
$KUBECTL --kubeconfig $KUBECONFIG delete -f /tmp/app/service.yaml --ignore-not-found || true
echo "✅ Cleanup completed!"
