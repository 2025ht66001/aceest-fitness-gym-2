pipeline {
  agent any

  environment {
    REGISTRY_CREDENTIALS = credentials('dockerhub-credentials-id') // set in Jenkins
    DOCKER_IMAGE = "2025ht66001/aceest-fitness"
    DOCKER_TAG = "${env.BUILD_NUMBER}"
    KUBE_CONTEXT = "minikube" // or your kube context
    SONARQUBE_SERVER = 'sonarqube-server-name' // Jenkins global tool
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt'
      }
    }

    stage('Unit Tests') {
      steps {
        sh '. .venv/bin/activate && pytest -q --cov=.'
      }
      post {
        always {
          junit '**/pytest*.xml'
        }
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('sonarqube-server-name') {
          sh '''
          . .venv/bin/activate
          pip install sonar-scanner-cli-python
          sonar-scanner \
            -Dsonar.projectKey=aceest-fitness \
            -Dsonar.python.version=3.12 \
            -Dsonar.sources=. \
            -Dsonar.tests=tests \
            -Dsonar.python.coverage.reportPaths=coverage.xml || true
          '''
        }
      }
    }

    stage('Build Image') {
      steps {
        sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG -t $DOCKER_IMAGE:latest .'
      }
    }

    stage('Push Image') {
      steps {
        sh 'echo $REGISTRY_CREDENTIALS_PSW | docker login -u $REGISTRY_CREDENTIALS_USR --password-stdin'
        sh 'docker push $DOCKER_IMAGE:$DOCKER_TAG'
        sh 'docker push $DOCKER_IMAGE:latest'
      }
    }

    stage('Deploy to Kubernetes (Rolling)') {
      steps {
        sh '''
        kubectl apply -f k8s/base/namespace.yaml
        kubectl apply -f k8s/base/deployment.yaml
        kubectl apply -f k8s/base/service.yaml
        kubectl apply -f k8s/base/ingress.yaml || true
        '''
      }
    }
  }

  post {
    success {
      echo "Build ${env.BUILD_NUMBER} deployed."
    }
    failure {
      echo "Build failed."
    }
  }
}
