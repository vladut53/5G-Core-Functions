pipeline {
    agent {
        node {
            label 'docker'
        }
    }
    stages {
        stage('run collection') {
            steps {
                script {
                    // Pull the Docker image containing Newman
                    docker.image('postman/newman').pull()

                    // Run Newman commands
                    docker.image('postman/newman').inside('-v ${WORKSPACE}:/etc/newman --workdir /etc/newman') {
                        sh 'newman run collection-2.json --color off --disable-unicode'
                    }
                }
            }
        }
    }
}
