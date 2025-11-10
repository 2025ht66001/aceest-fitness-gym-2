# ACEest Fitness & Gym — DevOps CI/CD

This repository contains a minimal Flask API and a complete CI/CD scaffold (Jenkins, Docker, Kubernetes) to satisfy the assignment requirements.

## Quickstart (Local)

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:8080/
```

## Docker

```bash
docker build -t your-dockerhub-username/aceest-fitness:latest .
docker run -p 8080:8080 your-dockerhub-username/aceest-fitness:latest
```

## Tests

```bash
pytest -q
```

## Kubernetes (Minikube)

```bash
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml
# optional ingress if NGINX ingress controller installed
kubectl apply -f k8s/base/ingress.yaml
```

See `k8s/blue-green`, `k8s/canary`, `k8s/shadow`, and `k8s/ab-testing` for progressive strategies.
