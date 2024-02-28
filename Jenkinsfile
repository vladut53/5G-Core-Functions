pipeline {
    agent any
    
    stages {
        stage('Print Workspace') {
            steps {
                // Print workspace directory content
                sh 'ls -la ${WORKSPACE}'
            }
        }
        
        stage('Copy File to Container') {
            steps {
                // Copy the JSON file from workspace to Docker container
                sh "docker cp ${WORKSPACE}/RF_NF_REGISTER.postman_collection.json CONTAINER_ID:/etc/newman/RF_NF_REGISTER.postman_collection.json"
            }
        }
        
        stage('Run Collection') {
            steps {
                // Execute Docker commands to run Postman collection
                sh "docker run -v ${WORKSPACE}:/etc/newman --workdir /etc/newman -t postman/newman run /etc/newman/RF_NF_REGISTER.postman_collection.json --color off --disable-unicode"
            }
        }
    }
}
