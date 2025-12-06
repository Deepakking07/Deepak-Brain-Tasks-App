import os
import boto3
import subprocess
import tempfile

def lambda_handler(event, context):
    """
    Lambda handler to deploy Kubernetes manifests to EKS without using AWS CLI
    """

    cluster_name = "brain-task-App"
    region_name = "us-east-1"

    # Paths
    kubectl = "/tmp/app/kubectl"
    kubeconfig = "/tmp/.kube/config"

    # Create kubeconfig directory
    os.makedirs(os.path.dirname(kubeconfig), exist_ok=True)

    # --- Step 1: Get EKS cluster info using boto3 ---
    eks = boto3.client("eks", region_name=region_name)
    cluster_info = eks.describe_cluster(name=cluster_name)["cluster"]
    endpoint = cluster_info["endpoint"]
    ca_data = cluster_info["certificateAuthority"]["data"]

    # --- Step 2: Create kubeconfig manually ---
    kubeconfig_content = f"""
apiVersion: v1
clusters:
- cluster:
    server: {endpoint}
    certificate-authority-data: {ca_data}
  name: {cluster_name}
contexts:
- context:
    cluster: {cluster_name}
    user: aws
  name: {cluster_name}
current-context: {cluster_name}
kind: Config
preferences: {{}}
users:
- name: aws
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: aws
      args:
        - "eks"
        - "get-token"
        - "--cluster-name"
        - "{cluster_name}"
        - "--region"
        - "{region_name}"
"""
    with open(kubeconfig, "w") as f:
        f.write(kubeconfig_content)

    # --- Step 3: Apply Kubernetes manifests ---
    manifests = ["/tmp/app/deployment.yaml", "/tmp/app/service.yaml"]
    for manifest in manifests:
        subprocess.run(
            [kubectl, "--kubeconfig", kubeconfig, "apply", "--validate=false", "-f", manifest],
            check=True
        )

    # --- Step 4: Return success ---
    return {
        "statusCode": 200,
        "body": "Deployment successful!"
    }

