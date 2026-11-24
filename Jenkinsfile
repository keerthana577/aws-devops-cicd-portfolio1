pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devops-demo-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        // Set these in the Jenkins job environment when publishing:
        // DOCKERHUB_USER and PUSH_IMAGE=true
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh '. .venv/bin/activate && pytest -q'
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Push image (optional)') {
            when {
                expression { return env.PUSH_IMAGE == 'true' }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG"
                        docker push "$DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG"
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
            cleanWs()
        }
    }
}
