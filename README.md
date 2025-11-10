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
docker build -t  2025ht66001/aceest-fitness:latest .
docker run -p 8080:8080  2025ht66001/aceest-fitness:latest
```

## Docker repo screenshot
<img width="1908" height="1158" alt="image" src="https://github.com/user-attachments/assets/40fdb914-52fd-4ae9-ba50-b8110e8b971f" />


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
