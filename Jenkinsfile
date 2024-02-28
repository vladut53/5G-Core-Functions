pipeline {
    agent any
    
    stages {
        stage('Print Workspace') {
            steps {
                // Print workspace directory content
                sh 'ls -la ${WORKSPACE}'
            }
        }
        
        stage('Run Collection') {
            steps {
                // Execute Docker commands to run Postman collection
                sh "docker run -v ${WORKSPACE}:/etc/newman --workdir /etc/newman -t postman/newman run 5G-Core-Functions/collection-2.json --color off --disable-unicode"
            }
        }
    }
}
