pipeline {
    agent any

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
    }
}
