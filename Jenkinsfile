pipeline {
    agent any
    stages {
        stage('Install Docker') {
            steps {
                // Install Docker using package manager (apt-get for Ubuntu)
                sh 'apt-get update && apt-get install -y docker.io'
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
