pipeline {
    agent any
    tools {
        // Use the Docker tool installation named "Local Docker"
        dockerTool 'Local Docker'
    }
    stages {
        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Example Docker commands
                    sh 'docker build -t my-image .'
                    sh 'docker push my-image'
                }
            }
        }
    }
}
