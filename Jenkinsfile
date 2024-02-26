pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'maven:3-alpine'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            agent any
            steps {
                sh 'mvn test'
            }
        }
    }
}
s
