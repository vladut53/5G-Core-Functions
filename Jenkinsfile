pipeline {
    agent any
    stages {
        stage('Install Docker') {
            steps {
                script {
                    // Use Docker plugin to install Docker
                    docker.withTool('docker') {
                        sh 'docker --version' // Just to verify Docker is installed
                    }
                }
            }
        }
        stage('run collection') {
            steps {
                // Run Docker commands now that Docker is installed
                sh 'docker run -t postman/newman run -h'
                sh 'docker run -v ${WORKSPACE}:/etc/newman --workdir /etc/newman -t postman/newman run NRF_NF_REGISTER.postman_collection.json --color off --disable-unicode'
            }
        }
    }
}
