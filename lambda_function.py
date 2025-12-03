import os
import boto3
import subprocess

def lambda_handler(event, context):
    """
    Lambda handler to deploy Kubernetes manifests to EKS
    """
    # Paths
    aws_cli = "/opt/awscli/bin/aws"   # Corrected path
    kubectl = "/tmp/app/kubectl"
    kubeconfig = "/tmp/.kube/config"
    
    # Create kubeconfig directory
    os.makedirs(os.path.dirname(kubeconfig), exist_ok=True)
    
    # Update kubeconfig for EKS
    subprocess.run([
        aws_cli, "eks", "update-kubeconfig",
        "--region", "us-east-1",                 # UPDATED REGION
        "--name", "brain-task-App",              # UPDATED CLUSTER NAME
        "--kubeconfig", kubeconfig
    ], check=True)
    
    # Apply Kubernetes manifests
    subprocess.run([
        kubectl, "--kubeconfig", kubeconfig,
        "apply", "--validate=false", "-f", "/tmp/app/deployment.yaml"
    ], check=True)
    
    subprocess.run([
        kubectl, "--kubeconfig", kubeconfig,
        "apply", "--validate=false", "-f", "/tmp/app/service.yaml"
    ], check=True)
    
    return {
        'statusCode': 200,
        'body': 'Deployment successful!'
    }

