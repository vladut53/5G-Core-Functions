pipeline {
    agent any
    stages {
        stage('Debug') {
            steps {
                script {
                    // Print contents of workspace directory
                    sh 'ls -la ${WORKSPACE}'
                }
            }
        }
        stage('Run Newman Tests') {
            steps {
                script {
                    // Run Newman tests using Docker command
                    sh 'docker run -v "$(pwd):/etc/newman" --workdir /etc/newman -t postman/newman run ./NRF_NF_REGISTER.json --color off --disable-unicode'
                }
            }
        }
    }
}
