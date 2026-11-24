# AWS DevOps CI/CD Automation Portfolio

A hands-on portfolio project demonstrating a containerized Python application, automated CI/CD, infrastructure as code, Kubernetes deployment, and application monitoring.

> **Portfolio / lab project:** This repository is intended for learning, demonstration, and interview discussion. It does not claim production deployment or professional experience with every included tool.

## Architecture

```text
Developer
   |
   v
GitHub repository
   |
   v
Jenkins pipeline
   |-- install dependencies + run tests
   |-- build Docker image
   |-- push image to Docker Hub (optional)
   |
   v
Kubernetes (local cluster or Amazon EKS)
   |-- Deployment (2 replicas)
   |-- Service
   |-- ConfigMap
   |-- readiness/liveness probes
   |
   v
Flask application (/ and /health)

Terraform folder: reusable starter configuration for provisioning an AWS EKS cluster.
Monitoring folder: Prometheus scrape configuration and Kubernetes deployment example.
```

## Repository contents

- `app/`: Flask application with health and Prometheus metrics endpoints.
- `tests/`: basic automated tests.
- `Dockerfile`: multi-stage image build.
- `Jenkinsfile`: CI pipeline with test, build, and optional Docker Hub push.
- `.github/workflows/ci.yml`: GitHub Actions validation workflow.
- `k8s/`: Kubernetes Deployment, Service, and ConfigMap.
- `terraform/eks/`: Terraform starter configuration using the official AWS EKS module.
- `monitoring/`: Prometheus configuration and deployment example.

## Prerequisites

- Git and GitHub account
- Python 3.11+ (for running locally)
- Docker
- Jenkins (for the Jenkins pipeline)
- kubectl and a Kubernetes cluster (Minikube, kind, or Amazon EKS)
- Terraform 1.5+ (only for the optional EKS infrastructure folder)
- AWS CLI configured with an IAM identity that has permissions to create EKS infrastructure (only if creating AWS resources)

## 1. Run locally

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python app/main.py
```

Open `http://127.0.0.1:5000/` and `http://127.0.0.1:5000/health`.

Run tests:

```bash
pytest -q
```

## 2. Build and run with Docker

```bash
docker build -t devops-demo-app:1.0 .
docker run --rm -p 5000:5000 devops-demo-app:1.0
```

Test:

```bash
curl http://localhost:5000/health
```

## 3. Deploy to Kubernetes

The default manifest uses a sample image name. Build and push your image to a registry, then update the `image` field in `k8s/deployment.yaml`.

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get pods
kubectl get deployments
kubectl get services
kubectl port-forward service/devops-demo-service 8080:80
```

Open `http://localhost:8080/`.

To update the image:

```bash
kubectl set image deployment/devops-demo app=<your-dockerhub-username>/devops-demo-app:1.0
kubectl rollout status deployment/devops-demo
kubectl rollout history deployment/devops-demo
```

Rollback if needed:

```bash
kubectl rollout undo deployment/devops-demo
```

## 4. Jenkins pipeline

1. Install Jenkins and the Pipeline, Git, and Docker-related integrations required by your Jenkins setup.
2. Create a Jenkins Pipeline job pointing to this GitHub repository.
3. Configure a Jenkins credential with ID `dockerhub-creds` (username/password or access token) if you want to push images.
4. Set the job environment variables `DOCKERHUB_USER` and `PUSH_IMAGE=true`.
5. Ensure the Jenkins agent has Docker available and permission to run it.
6. Run the pipeline.

The pipeline always runs tests and builds the image. It pushes only when `PUSH_IMAGE=true` and the Docker Hub credential is configured.

## 5. GitHub Actions

The workflow in `.github/workflows/ci.yml` runs on pushes and pull requests. It installs Python dependencies and runs the test suite.

## 6. Optional: create an AWS EKS cluster with Terraform

**Cost warning:** EKS and its supporting AWS resources can incur charges even when the demo application is idle. Review the plan and AWS pricing before applying. Destroy lab resources when finished.

```bash
cd terraform/eks
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with a unique cluster name and AWS region.
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

Configure kubectl after the cluster is created:

```bash
aws eks update-kubeconfig --region <region> --name <cluster-name>
kubectl get nodes
```

When finished with the lab:

```bash
terraform destroy
```

Do not commit `terraform.tfvars`, state files, credentials, kubeconfig files, or secrets.

## Interview walkthrough

A concise way to describe this portfolio:

"I created a hands-on DevOps portfolio project around a small Python web application. I containerized it using Docker, added automated tests and a Jenkins pipeline, and prepared Kubernetes manifests with health probes and multiple replicas. I also included Terraform starter code for an EKS cluster and a Prometheus monitoring example. The purpose was to practice the end-to-end workflow from source control to container build and Kubernetes deployment."

Be transparent about what you have personally run. If you have only reviewed a component's configuration, say that it is included as a learning extension rather than claiming production experience.

## Troubleshooting checklist

- **Docker build fails:** inspect the build output, dependency versions, and Docker daemon status.
- **Pod ImagePullBackOff:** verify image name/tag, registry visibility, and image pull credentials.
- **Pod CrashLoopBackOff:** use `kubectl logs <pod>` and `kubectl describe pod <pod>`.
- **Service not reachable:** check pod labels/selectors, endpoints, service port, and readiness.
- **Jenkins cannot access Docker:** verify Docker is installed on the agent and the Jenkins user has the required permissions.
- **Terraform access denied:** verify the active AWS identity and required IAM permissions.

## Security notes

- Never hardcode AWS keys, Docker Hub passwords, or application secrets.
- Use Jenkins Credentials for pipeline secrets.
- Use IAM roles and least-privilege permissions for AWS access.
- Pin and scan container dependencies/images before production use.
- The example Kubernetes ConfigMap is for non-sensitive configuration only.
