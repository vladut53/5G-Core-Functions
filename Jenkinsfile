pipeline {
    agent any
    stages {
        stage('run collection') {
            steps {
                script {
                    // Pull the Docker image containing Newman
                    docker.image('postman/newman').pull()

                    // Run Newman commands
                    docker.image('postman/newman').inside('-v ${WORKSPACE}:/etc/newman --workdir /etc/newman') {
                        sh 'newman run NRF_NF_REGISTER.postman_collection.json --color off --disable-unicode'
                    }
                }
            }
        }
    }
}
