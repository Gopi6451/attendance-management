pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = '755332618816.dkr.ecr.ap-south-1.amazonaws.com/attendance-management'
        IMAGE_TAG = 'latest'
    }

    
    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t attendance-management:latest .'
            }
        }

        stage('Docker Test') {
            steps {
                sh 'docker images attendance-management'
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin \
                    755332618816.dkr.ecr.ap-south-1.amazonaws.com
                '''
            }
        }

        stage('Docker Tag') {
            steps {
                sh '''
                    docker tag attendance-management:latest \
                    $ECR_REPOSITORY:$IMAGE_TAG
                '''
            }
        }

        stage('Docker Push') {
            steps {
                sh '''
                    docker push $ECR_REPOSITORY:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker pull $ECR_REPOSITORY:$IMAGE_TAG
        
                    docker stop attendance-management || true
                    docker rm attendance-management || true
        
                    docker run -d \
                      --name attendance-management \
                      -p 8000:8000 \
                      $ECR_REPOSITORY:$IMAGE_TAG
                '''
            }
        }
    }
}
