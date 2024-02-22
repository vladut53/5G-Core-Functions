pipeline {
    agent any
    stages {
        stage('Run Newman Tests') {
            steps {
                script {
                    // Pull the Newman image
                    sh 'docker pull postman/newman'

                    // Run Newman within Docker container
                    sh 'docker run -v ${pwd}:/etc/newman --workdir /etc/newman -t postman/newman run NRF_NF_REGISTER.json --color off --disable-unicode'
                }
            }
        }
    }
}
