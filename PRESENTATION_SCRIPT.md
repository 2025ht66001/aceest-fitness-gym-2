# Presentation Script - ACEest Fitness CI/CD

## Slide 1: Introduction
Hello, I am presenting the end-to-end CI/CD pipeline built for the ACEest Fitness & Gym application. The goal was to automate development, testing, containerization, and deployment with reliability and zero-downtime rollouts.

## Slide 2: Architecture
- Source code in GitHub
- Jenkins for CI/CD automation
- SonarQube for static code analysis
- Docker for containerization
- AWS ECR/Docker Hub for image storage
- Kubernetes on AWS (EKS) for deployment
- AWS ALB Ingress for traffic management

## Slide 3: Pipeline Workflow
1. Developer pushes code to GitHub
2. Jenkins triggers build automatically
3. Pytest executes unit tests
4. SonarQube performs code quality checks
5. Docker image is built and pushed to Docker Hub (2025ht66001/aceest-fitness)
6. Kubernetes rolling deployment updates the application with zero downtime

## Slide 4: Deployment Strategies Implemented
- Rolling Update (default)
- Blue-Green deployment for safe version switching
- Canary release using weighted routing via AWS ALB
- A/B testing via header-based routing ("X-Variant" header)

## Slide 5: Rollback Strategy
- For Rolling updates: `kubectl rollout undo`
- For Blue-Green: Switch service selector to previous version
- For Canary: Adjust weight to 100/0
- For A/B: Remove header routing rule

## Slide 6: Benefits
- Automated, repeatable deployments
- Faster release cycles
- Reduced risk through phased rollout strategies
- Clear quality gates (tests + SonarQube)
- Cloud-native scalability on Kubernetes

Thank you.
