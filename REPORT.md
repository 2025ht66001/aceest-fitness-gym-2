# CI/CD Architecture Overview

**Code** lives in GitHub with branches:
- `main` — production, protected.
- `develop` — integration.
- `feature/` —  features.
- Tags and releases are created in github repo for each versions of app

**Jenkins** runs a declarative pipeline on each PR/commit:
1. Checkout
2. Build Python venv & install deps
3. Run **pytest** with coverage
4. Run **SonarQube** static analysis with quality gate
5. Build and tag Docker image (`:BUILD_NUMBER` and `:latest`)
6. Push to Docker Hub
7. Deploy to Kubernetes (Rolling strategy by default)

**Kubernetes** hosts the Flask API. Readiness/liveness probes ensure zero-downtime rolling updates. Namespace `aceest` isolates resources.

**Container Registry:** Docker Hub maintains versioned images for traceability.

---

# Deployment Strategies Implemented

1. **Rolling Update (Default)**  
   In `k8s/base/deployment.yaml`, `strategy: RollingUpdate` with `maxSurge:1` and `maxUnavailable:0` ensures no downtime.

2. **Blue-Green**  
   Two Deployments: `aceest-api-blue` and `aceest-api-green`. The Service selector points to one label at a time (`version: blue/green`). Switch Service label to flip traffic instantly and enable instant rollback.

3. **Canary Release**  
   A secondary Deployment `aceest-api-canary` and Service with NGINX Ingress canary annotations (`canary-weight`). Adjust weight from 1% to 50% to 100% to graduate.

4. **Shadow (Mirroring)**  
   NGINX Ingress annotation `mirror-target` duplicates live traffic to `aceest-svc-shadow` for observation without user impact.

5. **A/B Testing**  
   Header-based routing using NGINX `configuration-snippet`. Requests with `X-Variant: B` go to variant B service; others go to stable.

**Rollback**: revert Service selector (Blue-Green), set canary weight to 0 (Canary), or `kubectl rollout undo deployment/aceest-api` (Rolling).

---

# Challenges & Mitigations

- **Original code base is Tkinter GUI**, not web-native.  
  *Mitigation:* Introduced a minimal Flask API that models core workout operations, decoupled from GUI, enabling containerization and HTTP testing.

- **Test reliability** with in-memory state.  
  *Mitigation:* App factory pattern (`create_app`) ensures isolated state per test via `app.test_client()`.

- **Kubernetes traffic splitting requires ingress support**.  
  *Mitigation:* Provided NGINX-based manifests which work on Minikube with NGINX ingress controller. Alternatives include service mesh (Istio/Linkerd) for production-grade traffic shaping.

- **Secrets & credentials in CI**.  
  *Mitigation:* Use Jenkins credentials store for Docker Hub and Kubernetes context; no secrets committed.

---

# Key Automation Outcomes

- Fully automated **build-test-scan-package-deploy** pipeline via Jenkins.
- **Pytest** verifies CRUD endpoints and health checks on each commit.
- **SonarQube** enforces code quality gate before containerization.
- **Docker** image pushed with immutable build numbers for traceability.
- **Kubernetes** manifests for multiple progressive delivery patterns with clear rollback steps.
