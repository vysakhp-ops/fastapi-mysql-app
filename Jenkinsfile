pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi-mysql-app"
        DEPLOY_USER = "innovature"
        DEPLOY_HOST = "10.10.12.123"
        DEPLOY_PATH = "/opt/deploy"
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
                sh 'docker build -t $IMAGE_NAME:latest ./app'
            }
        }

        stage('Save Docker Image') {
            steps {
                sh 'docker save -o app-image.tar $IMAGE_NAME:latest'
            }
        }

        stage('Copy Image to Dev Server') {
            steps {
                sshagent(['deploy-ssh']) {
                    sh """
                        scp -o StrictHostKeyChecking=no app-image.tar $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/
                    """
                }
            }
        }

        stage('Load & Deploy on Dev Server') {
            steps {
                sshagent(['deploy-ssh']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST "
                            docker load -i $DEPLOY_PATH/app-image.tar &&
                            cd $DEPLOY_PATH &&
                            docker compose up -d
                        "
                    """
                }
            }
        }
    }
}

