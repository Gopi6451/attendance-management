pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = '755332618816.dkr.ecr.ap-south-1.amazonaws.com/attendance-management'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    
    
    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code - Webhook Test...'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t attendance-management:${BUILD_NUMBER} .'
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
                    docker tag attendance-management:${BUILD_NUMBER} \
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
                    kubectl set image deployment/attendance-management \
                    attendance-management=$ECR_REPOSITORY:$IMAGE_TAG

                    kubectl rollout status deployment/attendance-management

                    kubectl get pods
                '''
            }
        }   
    }
}
