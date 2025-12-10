pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi-mysql-app"
        DOCKER_USER = "vysakhpanilkumar97"
        DEPLOY_USER = "innovature"
        DEPLOY_HOST = "10.10.12.123"     // or the server IP
        DEPLOY_PATH = "/opt/deploy"   // folder where compose.yaml is stored
    }

    stages {

        stage('Checkout') {
            steps {
                git(
                    url: 'https://github.com/vysakhp-ops/fastapi-mysql-app.git',
                    branch: 'main',
                    credentialsId: 'github-creds'
                )
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_USER/$IMAGE_NAME:latest ./app'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-pass', variable: 'DOCKER_PASS')]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh 'docker push $DOCKER_USER/$IMAGE_NAME:latest'
            }
        }

        stage('Deploy to Dev Server') {
            steps {
                sshagent(['deploy-ssh']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST "
                            cd $DEPLOY_PATH &&
                            docker compose pull &&
                            docker compose up -d
                        "
                    """
                }
            }
        }
    }
}
